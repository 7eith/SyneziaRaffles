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

# from .aio_task import AIOTask
# from .create_account import CreateAccount
from .enter_raffle import EnterRaffle

from configuration.configuration import Configuration
from discord_webhook import DiscordWebhook, DiscordEmbed

import utilities
import time

# from notifier import NotifyCreatedAccount

class RaffleModule():

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

		# if (state == "CREATED"):
		# 	NotifyCreatedAccount(profile, "StreetMachine")

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
		Instance().updateRPC("Running StreetMachine")
		
		version = "0.0.1"
		moduleName = "StreetMachine"
		action = "Enter_Raffle"
		date = Instance().getDate()
		self.loggerFileName = f"logs/{moduleName}/{action}_{date}.csv"

		if (not Configuration().two_captcha):
			Logger.error("Invalid 2Captcha Key... Exiting CLI in 45s. Edit your settings file!")
			time.sleep(45)
			exit(0)
			return 

		""" Status """
		successTask: int = 0
		failedTask: int = 0

		""" Proxies """
		proxies = ProxyManager(moduleName)

		""" Profiles """
		profile = Profile(moduleName)
		profiles = profile.fetchProfiles()

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
		Logger.info(">> Proxies: {} [{}]".format(proxies.proxiesFile, len(proxies.getProxies())))
		Logger.info(">> Log File: {}\n".format(f"{action}_{date}.csv"))
		utilities.printLine()

		for index, profile in enumerate(profiles):
			print("")
			utilities.printLine()

			task = EnterRaffle(index, profile, self.loggerFileName, user_agent_rotator.get_random_user_agent())

			if (task.success):
				successTask += 1
				self.__successTask(index, profile, task.state)
				
			else:
				failedTask += 1
				self.__failTask(index, profile, task.state)			

			remaining = len(profiles) - (index + 1)
			utilities.setTitle(f"SyneziaRaffle - StreetMachine / Success: {str(successTask)} - Failed {str(failedTask)} - Remaining {str(remaining)}")
			
		""" Retrying? """
		utilities.setTitle(f"SyneziaRaffle [Finish] - StreetMachine / Success: {str(successTask)} - Failed {str(failedTask)}")

		""" UI """
		Logger.success(f"Task has finished. Success: Success: {str(successTask)} - Failed {str(failedTask)}")
		print("")
		Logger.info(f"Choosing what to do...")
		Logger.info(f"1. Retrying failed tasks [{str(failedTask)}]")
		Logger.info(f"2. Exit.")
		res = input(f"\n")

		""" Want to retry failed tasks """
		if (res and res[0] == "1"):
			utilities.setTitle(f"SyneziaRaffle [Running Failed Tasks] - StreetMachine / Success: {str(successTask)} - Failed {str(failedTask)}")

			successTask = 0
			failedTask = 0
			utilities.printHeader()

			""" Loop """
			for index, profile in enumerate(profiles):
				if ("success" not in profile or not profile['success']):
					print("")
					utilities.printLine()

					task = EnterRaffle(index, profile, self.loggerFileName, user_agent_rotator.get_random_user_agent())

					if (task.success):
						successTask += 1
						self.__successTask(index, profile, task.state)
						
					else:
						failedTask += 1
						self.__failTask(index, profile, task.state)			

					remaining = len(profiles) - (index + 1)
					utilities.setTitle(f"SyneziaRaffle [Running Failed Tasks] - StreetMachine / Success: {str(successTask)} - Failed {str(failedTask)} - Remaining {str(remaining)}")
					
		utilities.setTitle(f"SyneziaRaffle [Finished Failed Tasks] - StreetMachine / Success: {str(successTask)} - Failed {str(failedTask)}")
		Logger.success(f"Task has finished. Success: Success: {str(successTask)} - Failed {str(failedTask)}")
		Logger.info("Press Enter to exit CLI.")
		input("")