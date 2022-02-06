'''

[raffle] NakedRaffle.py

Author: seith <seith.corp@gmail.com>

Created: 09/05/2021 02:44:46 by seith
Updated: 09/05/2021 02:44:46 by seith

Synezia Corp. (c) 2021 - MIT

'''

import PyInquirer
import requests
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

from notifier import NotifyEnterRaffle
from twocap import TwoCaptcha


from .EnterRaffle import EnterRaffle

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

class NakedRaffle():

	def getAvailableRaffle(self):
		try:
			raffles = requests.get("https://raw.githubusercontent.com/iSnkh/isnkh.github.io/v2/assets/utils/snz").json()['raffles']
		except Exception as error:
			Logger.error(error)
			return self.getAvailableRaffle()

		return (raffles)

	def selectRaffles(self):
		raffles = self.getAvailableRaffle()

		questions = [
			{
				'type': 'list',
				'name': 'choice',
				'message': 'Select Raffle...',
				'choices': raffles
			}
		]

		answer = PyInquirer.prompt(
			questions=questions,
			keyboard_interrupt_msg=f"Cancelled by User. Exiting CLI",
		).get("choice")

		if not answer:
			exit(0)

		raffle = [element for element in raffles if answer == element['name']]
		self.raffle = raffle[0]

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
			NotifyEnterRaffle(profile, "Naked", self.raffle['image'], self.raffle['name'])

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
		moduleName = "Naked"
		action = "Enter_Raffle"
		version = "0.0.1"
		date = Instance().getDate()
		self.loggerFileName = f"logs/{moduleName}/{action}_{date}.csv"
		self.twoCaptcha = TwoCaptcha(Configuration().two_captcha)

		""" UI """
		printHeader()
		Instance().updateRPC(f"Running Naked")
		utilities.setTitle(f"SyneziaRaffle - Running Naked")

		""" Status """
		successTask: int = 0
		failedTask: int = 0

		self.selectRaffles()

		""" Load Files """
		profile = Profile(moduleName)
		profiles = profile.fetchProfiles()
		profileName = os.path.basename(profile.profileFile).split('.')[0]
		profileLen = len(profiles)

		proxies = ProxyManager(moduleName)

		self.promptDelay()

		""" ASSETS """
		Logger.info("[2Captcha] Your balance is {}$".format(str(self.twoCaptcha.balance())))
		Logger.info("Initializating assets...")

		from random_user_agent.user_agent import UserAgent
		user_agent_rotator = UserAgent(software_names=['chrome', 'firefox'], operating_systems=['windows', 'linux', 'macos'])
		createFileLogger(self.loggerFileName, profiles[0].keys())


		for index, profile in enumerate(profiles):
			print("")
			utilities.printLine()

			task = EnterRaffle(index, profile, self.raffle, user_agent_rotator.get_random_user_agent())

			if (task.success):
				successTask += 1
				self.__successTask(index, profile, task.status)
				
			else:
				failedTask += 1
				self.__failTask(index, profile, task.status)		

			remaining = profileLen - (index + 1)
			utilities.setTitle(f"SyneziaRaffle [Naked] / Success: {str(successTask)} - Failed {str(failedTask)} - Remaining {str(remaining)} / 2Captcha Balance: {str(self.twoCaptcha.balance())}")
			
			delay = random.randint(self.minDelay, self.maxDelay)
			Logger.info(f"Waiting {delay} to do another Task...")
			time.sleep(delay)	

		input("Press Enter to close CLI")