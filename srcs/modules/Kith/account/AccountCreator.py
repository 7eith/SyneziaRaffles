'''

[raffle] NakedRaffle.py

Author: seith <seith.corp@gmail.com>

Created: 09/05/2021 02:44:46 by seith
Updated: 09/05/2021 02:44:46 by seith

Synezia Corp. (c) 2021 - MIT

'''

import PyInquirer
import os
import time 
import random 

import utilities
from singleton import Instance
from profiles import Profile

from configuration.configuration import Configuration
from utils.cli_utils import printHeader
from utils.colors import Color
from logger import Logger, createFileLogger

from proxy.controller import ProxyManager

from notifier import NotifyCreatedAccount
from .create_account import CreateAccount

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

class KithAccountCreator():

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
			NotifyCreatedAccount(profile, "Kith")

	def __failTask(self, index, profile, state):
		try:
			f = open(self.loggerFileName, 'a')
			csvLine = f"{state},"
			csvLine += ",".join(profile.values())
			f.write(f"{csvLine}\n")
			f.close()
		except Exception as error:
			Logger.error(error)
	
	def __init__(self):
		moduleName = "Kith"
		action = "Create_Account"
		version = "0.0.1"
		date = Instance().getDate()
		self.loggerFileName = f"logs/{moduleName}/{action}_{date}.csv"

		""" UI """
		printHeader()
		Instance().updateRPC(f"Running Kith [EU]")
		utilities.setTitle(f"SyneziaRaffle - Kith [EU]")

		""" Status """
		successTask: int = 0
		failedTask: int = 0

		""" Load Files """
		profile = Profile(moduleName)
		profiles = profile.fetchProfiles()
		profileName = os.path.basename(profile.profileFile).split('.')[0]
		profileLen = len(profiles)

		proxies = ProxyManager(moduleName)

		self.promptDelay()

		""" ASSETS """
		Logger.info("Initializating assets...")

		from random_user_agent.user_agent import UserAgent
		user_agent_rotator = UserAgent(software_names=['chrome', 'firefox'], operating_systems=['windows', 'linux', 'macos'])
		createFileLogger(self.loggerFileName, profiles[0].keys())

		for index, profile in enumerate(profiles):
			print("")
			utilities.printLine()

			task = CreateAccount(index, profile, user_agent_rotator.get_random_user_agent())

			if (task.success):
				successTask += 1
				self.__successTask(index, profile, task.status)
				
			else:
				failedTask += 1
				self.__failTask(index, profile, task.status)		

			remaining = profileLen - (index + 1)
			utilities.setTitle(f"SyneziaRaffle [Kith] / Success: {str(successTask)} - Failed {str(failedTask)} - Remaining {str(remaining)}")
			
			delay = random.randint(self.minDelay, self.maxDelay)
			Logger.info(f"[{index}] Waiting {delay}s")
			time.sleep(delay)	

		input("Press Enter to close CLI")