'''

[raffle] raffle_module.py

Author: seith <seith.corp@gmail.com>

Created: 11/04/2021 20:15:52 by seith
Updated: 11/04/2021 20:15:52 by seith

Synezia Corp. (c) 2021 - MIT

'''

import PyInquirer

from singleton import Instance
from profiles import Profile

from proxy.controller import ProxyManager
from utils.colors import Color
from logger.logger import Logger

from concurrent.futures import ThreadPoolExecutor, as_completed

from .enter_raffle import EnterRaffle

from configuration.configuration import Configuration

import utilities
import time
import os
import random

class NumberValidator(PyInquirer.Validator):
	def validate(self, document):
		try:
			int(document.text)
		except ValueError:
			raise PyInquirer.ValidationError(
				message='Please enter a number',
				cursor_position=len(document.text))  # Move cursor to end

class RaffleModule():

	def __createLogger(self, loggerFileName):
		header = "status,firstName,lastName,email,zipCode,phone,size"

		try:
			f = open(loggerFileName, 'a')
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
		version = "0.0.1"
		moduleName = "TravisScott"
		action = "Enter_Raffle"
		date = Instance().getDate()
		self.loggerFileName = f"logs/{moduleName}/{action}_{date}.csv"

		Instance().updateRPC(f"Running TravisScott...")

		""" Status """
		successTask: int = 0
		failedTask: int = 0

		""" Proxies """
		proxies = ProxyManager(moduleName)

		""" Profiles """
		profile = Profile(moduleName)
		profiles = profile.fetchProfiles()
		profileLen = len(profiles)
		profileName = os.path.basename(profile.profileFile).split('.')[0]
		random.shuffle(profiles)

		questions = [
			{
				'type': 'input',
				'name': 'quantity',
				'message': 'How much thread to run?',
				'validate': NumberValidator,
				'filter': lambda val: int(val)
			}
		]

		threadNumber = PyInquirer.prompt(questions)['quantity']

		""" Create Logger """

		self.__createLogger(self.loggerFileName)

		""" Print """
		utilities.printHeader()
		utilities.printLine()

		tasks = []

		with ThreadPoolExecutor(max_workers=threadNumber) as executor:
			for index, profile in enumerate(profiles):

				tasks.append(executor.submit(EnterRaffle, index, profile))

			for task in as_completed(tasks):
				try:

					TaskResult = task.result()

					if (TaskResult.success):
						successTask += 1

						self.__successTask(TaskResult.index, TaskResult.profile, TaskResult.state)
					else:
						failedTask += 1
						self.__failTask(TaskResult.index, TaskResult.profile, TaskResult.state)

				except Exception as error:
					Logger.error(error)
					failedTask += 1

				remaining = profileLen - (failedTask + successTask + 1)
				utilities.setTitle(f"Synezia - TravisScott [{profileName}] / Success: {str(successTask)} - Failed {str(failedTask)} - Remaining {str(remaining)}")
				
		""" Retrying? """
		utilities.setTitle(f"Synezia - TravisScott [Finish] - [{profileName}] FootLocker / Success: {str(successTask)} - Failed {str(failedTask)}")

		""" UI """
		Logger.success(f"Task has finished. Success: {str(successTask)} - Failed {str(failedTask)}")
		input("Close CLI?")