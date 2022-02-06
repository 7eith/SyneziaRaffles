'''

[account] account_module.py

Author: seith <seith.corp@gmail.com>

Created: 01/03/2021 15:05:49 by seith
Updated: 01/03/2021 15:05:49 by seith

Synezia Corp. (c) 2021 - MIT

'''

from utils.cli_utils import printHeader, printLine
from logger.logger import Logger
from proxy.controller import ProxyManager
from controller.profile_parser import fetchProfiles

from concurrent.futures import ThreadPoolExecutor, as_completed

from .create_account import CreateAccount

class FootLockerAccountCreaterModule:
	def __init__(self):

		"""
			UI
		"""

		printHeader()
		printLine()

		"""
			Proxy
		"""

		self.proxyManager = ProxyManager("FootLocker")
		self.proxy = self.proxyManager.getProxy()

		"""
			Profiles
		"""

		profiles = fetchProfiles("FootLocker")
		print("\n")
		printLine()

		"""
			Prompt Settings
		"""

		# TODO: HERE

		"""
			UI
		"""

		printHeader()
		printLine()

		"""
			HELLO MULTITHREADING
		"""

		Logger.info('Starting Generating!')

		processes = []
		with ThreadPoolExecutor(max_workers=500) as executor:
			for index, profile in enumerate(profiles):
				executor.submit(CreateAccount, index, profile)

		# for index, profile in enumerate(profiles):
		# 		CreateAccount(index, profile)
		# Logger.info('Finished!')

