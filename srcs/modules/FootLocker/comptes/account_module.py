'''

[account] account_module.py

Author: seith <seith.corp@gmail.com>

Created: 03/04/2021 18:08:54 by seith
Updated: 03/04/2021 18:08:54 by seith

Synezia Corp. (c) 2021 - MIT

'''
from singleton import Instance
from profiles import Profile

from proxy.controller import ProxyManager
from utils.colors import Color
from logger.logger import Logger

from .create_account import CreateAccount

from configuration.configuration import Configuration
from concurrent.futures import ThreadPoolExecutor, as_completed

import utilities
import time
import PyInquirer
import os

class NumberValidator(PyInquirer.Validator):
	def validate(self, document):
		try:
			int(document.text)
		except ValueError:
			raise PyInquirer.ValidationError(
				message='Please enter a number',
				cursor_position=len(document.text))  # Move cursor to end

class AccountModule():

	def __createLogger(self, loggerFileName):
		header = "status,first_name,last_name,email,password"

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
		Instance().updateRPC("Generating FootLocker...")
		
		version = "0.0.1"
		moduleName = "FootLocker"
		date = Instance().getDate()
		self.loggerFileName = f"logs/{moduleName}/created_account.csv"

		""" Status """
		successTask: int = 0
		failedTask: int = 0
		registeredTask: int = 0

		""" Proxies """
		if (not Configuration().proxyless):
			proxies = ProxyManager(moduleName)

		# os.path.basename('/users/system1/student1/homework-1.py')

		""" Profiles """
		profile = Profile(moduleName)
		profiles = profile.fetchProfiles()

		profileName = os.path.basename(profile.profileFile).split('.')[0]
		profileLen = len(profiles)

		""" Thread """
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

		""" UserAgent """
		Logger.info("Initializating assets...")
		from random_user_agent.user_agent import UserAgent
		user_agent_rotator = UserAgent(software_names=['chrome', 'edge', 'opera', 'firefox', 'android-browser'], operating_systems=['windows', 'linux', 'macos', 'android', 'ios'])
		
		""" Create Logger """

		self.__createLogger(self.loggerFileName)

		""" Print """
		utilities.printHeader()
		utilities.printLine()
		Logger.info("\t\t     [Resume]")
		Logger.info(">> Profile: {} [{}]".format(profile.profileFile, len(profiles)))
		if (not Configuration().proxyless):
			Logger.info(">> Proxies: {} [{}]".format(proxies.proxiesFile, len(proxies.getProxies())))
		Logger.info(">> Log File: {}\n".format(f"{self.loggerFileName}"))
		Logger.info(">> Thread(s): {}\n".format(f"{threadNumber}"))

		""" Proxyless ?"""
		if (Configuration().proxyless):
			Logger.info(">> Mode(s): {}\n".format(f"ProxyLess"))
		else:
			Logger.info(">> Mode(s): {}\n".format(f"using Proxy"))

		""" UI """
		utilities.printLine()
		utilities.setTitle(f"SyneziaRaffle - FootLocker [{profileName}] ")

		tasks = []

		with ThreadPoolExecutor(max_workers=threadNumber) as executor:
			for index, profile in enumerate(profiles):

				tasks.append(executor.submit(CreateAccount,index, profile, self.loggerFileName, user_agent_rotator.get_random_user_agent()))

			for task in as_completed(tasks):
				try:

					TaskResult = task.result()

					if (TaskResult.success):
						if (TaskResult.state == "CREATED"):
							successTask += 1
						else:
							registeredTask += 1

						self.__successTask(TaskResult.index, TaskResult.profile, TaskResult.state)
					else:
						failedTask += 1
						self.__failTask(TaskResult.index, TaskResult.profile, TaskResult.state)

				except Exception as error:
					Logger.error(error)
					failedTask += 1

				remaining = profileLen - (failedTask + successTask + 1 + registeredTask)
				utilities.setTitle(f"Synezia - [{profileName}] / Success: {str(successTask)} - Failed {str(failedTask)} - Remaining {str(remaining)}")
				
		""" Retrying? """
		utilities.setTitle(f"Synezia [Finish] - [{profileName}] FootLocker / Success: {str(successTask)} - Failed {str(failedTask)}")

		""" UI """
		Logger.success(f"Task has finished. Success: {str(successTask)} - Failed {str(failedTask)}")
		# print("")
		# Logger.info(f"Choosing what to do...")
		# Logger.info(f"1. Retrying failed tasks [{str(failedTask)}]")
		# Logger.info(f"2. Exit.")
		# res = input(f"\n")

		# """ Want to retry failed tasks """
		# if (res and res[0] == "1"):
		# 	utilities.setTitle(f"SyneziaRaffle [Running Failed Tasks] - StreetMachine / Success: {str(successTask)} - Failed {str(failedTask)}")

		# 	successTask = 0
		# 	failedTask = 0
		# 	utilities.printHeader()

		# 	""" Loop """
		# 	for index, profile in enumerate(profiles):
		# 		if ("success" not in profile or not profile['success']):
		# 			print("")
		# 			utilities.printLine()

		# 			task = CreateAccount(index, profile, self.loggerFileName, user_agent_rotator.get_random_user_agent())

		# 			if (task.success):
		# 				successTask += 1
		# 				self.__successTask(index, profile, task.state)
						
		# 			else:
		# 				failedTask += 1
		# 				self.__failTask(index, profile, task.state)			

		# 			remaining = len(profiles) - (index + 1)
		# 			utilities.setTitle(f"SyneziaRaffle [Running Failed Tasks] - StreetMachine / Success: {str(successTask)} - Failed {str(failedTask)} - Remaining {str(remaining)}")
					
		# utilities.setTitle(f"SyneziaRaffle [Finished Failed Tasks] - StreetMachine / Success: {str(successTask)} - Failed {str(failedTask)}")
		# Logger.success(f"Task has finished. Success: Success: {str(successTask)} - Failed {str(failedTask)}")
		# Logger.info("Press Enter to exit CLI.")
		# input("")