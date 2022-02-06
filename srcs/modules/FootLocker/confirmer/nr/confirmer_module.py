'''

[flx] flx_module.py

Author: seith <seith.corp@gmail.com>

Created: 13/04/2021 02:10:10 by seith
Updated: 13/04/2021 02:10:10 by seith

Synezia Corp. (c) 2021 - MIT

'''

from ..utils import readLinks
from .confirm_link import ConfirmLink

from singleton import Instance
from profiles import Profile

from proxy.controller import ProxyManager
from utils.colors import Color
from logger.logger import Logger

from configuration.configuration import Configuration
from concurrent.futures import ThreadPoolExecutor, as_completed

from notifier import NotifyEndConfirmations

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

class FootLockerLinkConfirmer():

	def __createLogger(self, loggerFileName):
		header = "status,first_name,last_name,email"

		try:
			f = open(loggerFileName, 'a')
			f.write(f"{header}\n")
			f.close()
		except Exception as error:
			Logger.error(error)

	def __successTask(self, index, profile, state):
		try:
			f = open(self.loggerFileName, 'a')
			f.write(f"{state},{profile['first_name']},{profile['last_name']},{profile['email']}\n")
			f.close()
		except Exception as error:
			Logger.error(error)

	def __failTask(self, link):
		try:
			f = open(self.failedFileName, 'a')
			f.write(f"{link}\n")
			f.close()
		except Exception as error:
			Logger.error(error)

	def __init__(self):
		Instance().updateRPC("Running FootLocker..")
		
		version = "0.0.1"
		moduleName = "FootLocker"
		date = Instance().getDate()

		""" Logger """
		self.loggerFileName = f"logs/{moduleName}/confirmed_accounts.csv"
		self.failedFileName = f"logs/{moduleName}/failed_links.txt"
		self.__createLogger(self.loggerFileName)

		""" Status """
		successTask: int = 0
		failedTask: int = 0

		""" Links """
		links = readLinks()
		linksLen = len(links)

		""" Proxies """
		if (not Configuration().proxyless):
			proxies = ProxyManager(moduleName)

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
		user_agent_rotator = UserAgent(software_names=['chrome', 'firefox'], operating_systems=['windows', 'linux', 'macos'])
		
		""" Print """
		utilities.printHeader()
		utilities.printLine()
		Logger.info("\t\t     [Resume]")
		if (not Configuration().proxyless):
			Logger.info(">> Proxies: {} [{}]".format(proxies.proxiesFile, len(proxies.getProxies())))
		Logger.info(">> Log File: {}".format(f"{self.loggerFileName}"))
		Logger.info(">> Thread(s): {}\n".format(f"{threadNumber}"))

		""" UI """
		utilities.printLine()
		utilities.setTitle(f"SyneziaRaffle - FootLocker [Confirmer]")

		tasks = []

		with ThreadPoolExecutor(max_workers=threadNumber) as executor:
			for index, link in enumerate(links):

				tasks.append(executor.submit(ConfirmLink, index, link,  user_agent_rotator.get_random_user_agent()))

			for index, task in enumerate(as_completed(tasks)):
				try:
					TaskResult = task.result()

					if (TaskResult.success):
						successTask += 1
						self.__successTask(TaskResult.index, TaskResult.profile, TaskResult.state)
					else:
						failedTask += 1
						self.__failTask(TaskResult.link)

				except IndexError as error:
					Logger.error(f"[{index}] Invalid link!")
					failedTask += 1

				except Exception as error:
					Logger.error(f"lol {error}")
					failedTask += 1

				remaining = linksLen - (failedTask + successTask + 1)
				utilities.setTitle(f"Synezia [FootLocker] - Confirmer / Success: {str(successTask)} - Failed {str(failedTask)} - Remaining {str(remaining)}")
				
		""" UI """
		utilities.setTitle(f"Synezia [Finish] - FootLocker / Success: {str(successTask)} - Failed {str(failedTask)}")
		NotifyEndConfirmations(successTask, failedTask)
		Logger.success(f"Task has finished. Success: {str(successTask)} - Failed {str(failedTask)}")
