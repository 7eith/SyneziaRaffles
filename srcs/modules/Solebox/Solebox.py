'''

[Solebox] Solebox.py

Author: seith <seith.corp@gmail.com>

Created: 23/04/2021 20:33:13 by seith
Updated: 23/04/2021 20:33:13 by seith

Synezia Corp. (c) 2021 - MIT

'''

import PyInquirer
import time
import os
import requests
import re
import random

import utilities

from singleton import Instance
from profiles import Profile
from .SoleboxLiveHelper import * 
from configuration.configuration import Configuration
from utils.cli_utils import printHeader
from utils.colors import Color
from logger.logger import Logger

from proxy.controller import ProxyManager

from notifier import NotifyEnterRaffle

from .enter_raffle import SoleboxEnterRaffle

class DelayValidator(PyInquirer.Validator):
	def validate(self, document):
		values = document.text.split(",")
		
		if (len(values) != 2):
			raise PyInquirer.ValidationError(
				message='Enter a delay in seconds like : 5, 45 (Must be an Number separated by comma)',
				cursor_position=len(document.text))  # Move cursor to end

		try:
			min = int(values[0])
			max = int(values[1])
		except ValueError:
			raise PyInquirer.ValidationError(
				message='Enter a delay in seconds like : 5, 45 (Must be an Number separated by comma)',
				cursor_position=len(document.text))  # Move cursor to end

class Solebox():

	def getAvailableRaffle(self):
		try:
			raffles = fetchSoleboxRaffles()

			for raffle in raffles:
				if checkRaffleAvailability(raffle):
					raffleData = parseSoleboxForm(raffle)
				else:
					raffle['disabled'] = "Closed"

			return (raffles)

		except Exception as error:
			Logger.error(f"Error has occured when fetching live raffles... {error}")
			Logger.error(f"{error}")
			self.retryTime += 1
			Logger.error(f"Retrying to fetch raffles... ({self.retryTime}/5 retry)")

			if (self.retryTime == 5):
				Logger.error("Max retries exceeded! Exiting Module...")
				return (False)
			else:
				return self.getAvailableRaffle()

	def promptDelay(self):

		questions = [
			{
				'type': 'input',
				'name': 'size',
				'message': 'Enter delay in seconds here (Separated by comma like 1,5)',
				'default': '5, 45',
				'validate': DelayValidator
			},
		]

		answer = (
			PyInquirer.prompt(questions=questions, keyboard_interrupt_msg=f"Cancelled by User. Exiting CLI")
			.get("size")
		)

		delayAnswer = answer.split(",")

		self.minDelay = int(delayAnswer[0])
		self.maxDelay = int(delayAnswer[1])

	def selectRaffles(self):
		questions = [
			{
				'type': 'list',
				'name': 'choice',
				'message': 'Select Raffle...',
				'choices': self.raffles
			}
		]

		answer = PyInquirer.prompt(
			questions=questions,
			keyboard_interrupt_msg=f"Cancelled by User. Exiting CLI",
		).get("choice")

		if not answer:
			exit(0)

		raffle = [element for element in self.raffles if answer == element['name']]
		self.raffle = raffle[0]

	def __createLogger(self, loggerFileName):
		header = "status,email,first_name,last_name,instagram,phone,month,day,shop,size,color"

		try:
			f = open(loggerFileName, 'w')
			f.write(f"{header}\n")
			f.close()
		except Exception as error:
			Logger.error(error)

	def __successTask(self, index, profile, state):
		try:
			f = open(self.loggerFileName, 'a')
			csvLine = f"{state},"
			csvLine += ",".join(profile.values())
			f.write(f"{csvLine}\n")
			f.close()
		except Exception as error:
			Logger.error(error)

		if (state == "SUCCESS"):
			NotifyEnterRaffle(profile, "Solebox", self.raffle['image'], self.raffle['name'])

	def __failTask(self, index, profile, state):
		try:
			f = open(self.loggerFileName, 'a')
			csvLine = f"{state},"
			csvLine += ",".join(profile.values())
			f.write(f"{csvLine}\n")
			f.close()
		except Exception as error:
			Logger.error(error)

	def checkProfile(self, index, profile):
		if (profile['size'] == "RANDOM"):
			profile['size'] = random.choice(self.raffle['params']['Sizes']['values'])

		if (profile['shop'] not in self.raffle['params']['Store']['values']):
			Logger.error(f"[{index}] Invalid Shop for {profile['email']}!")
			return (False)

		if (profile['size'] not in self.raffle['params']['Sizes']['values']):
			Logger.error(f"[{index}] Invalid Sizes for {profile['email']}!")
			return (False)
		

		return (True)

	def __init__(self):
		moduleName = "Solebox"
		action = "Enter_Raffle"
		version = "0.0.1"
		date = Instance().getDate()
		self.loggerFileName = f"logs/{moduleName}/{action}_{date}.csv"
		self.retryTime: int = 0

		""" UI """
		printHeader()
		Instance().updateRPC(f"Running Solebox...")
		utilities.setTitle(f"SyneziaRaffle - Running Solebox")
		
		""" Status """
		successTask: int = 0
		failedTask: int = 0

		Logger.info("Fetching Live Raffles...")
		self.raffles = self.getAvailableRaffle()

		if (self.raffles == False):
			return 

		Logger.success("Successfully fetched raffle in Live!\n") 
		self.selectRaffles()

		""" Proxies """
		proxies = ProxyManager(moduleName)

		""" Profiles """
		profile = Profile(moduleName)
		profiles = profile.fetchProfiles()

		profileName = os.path.basename(profile.profileFile).split('.')[0]
		profileLen = len(profiles)

		""" Settings """
		self.promptDelay()

		""" Assets """
		Logger.info("Initializating assets...")

		from random_user_agent.user_agent import UserAgent
		user_agent_rotator = UserAgent(software_names=['chrome', 'edge', 'opera', 'firefox'], operating_systems=['windows', 'linux', 'macos'])
		self.__createLogger(self.loggerFileName)

		for index, profile in enumerate(profiles):
			print("")
			utilities.printLine()

			if (self.checkProfile(index, profile)):
				task = SoleboxEnterRaffle(index, profile, self.raffle, user_agent_rotator.get_random_user_agent())

				if (task.success):
					successTask += 1
					self.__successTask(index, profile, task.status)
					
				else:
					failedTask += 1
					self.__failTask(index, profile, task.status)		
			else:
				failedTask += 1
				self.__failTask(index, profile, "INVALID")	

			remaining = profileLen - (index + 1)
			utilities.setTitle(f"SyneziaRaffle - / Success: {str(successTask)} - Failed {str(failedTask)} - Remaining {str(remaining)}")
			
			delay = random.randint(self.minDelay, self.maxDelay)
			Logger.info(f"Waiting {delay} to do another Task...")
			time.sleep(delay)	

		input("Press Enter to exit Module!")