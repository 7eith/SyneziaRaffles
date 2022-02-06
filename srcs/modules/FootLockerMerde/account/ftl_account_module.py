'''

[account] ftl_account_module.py

Author: seith <seith.corp@gmail.com>

Created: 15/02/2021 22:32:43 by seith
Updated: 15/02/2021 22:32:43 by seith

Synezia Corp. (c) 2021 - MIT

'''

import requests
import json
import inquirer
import glob
import random

from utils.cli_utils import printHeader, printLine
from logger.logger import Logger
from proxy.controller import ProxyManager
from controller.profile_parser import fetchProfiles

from .ftl_create_account import FootLockerCreateAccount
from concurrent.futures import ThreadPoolExecutor, as_completed


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

		self.proxyManager = ProxyManager()
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

		# for i, profile in enumerate(profiles):
		# FootLockerCheckAccount(i, profile)
		# FootLockerCheckAccount()

		# FootLockerCreateAccount(profiles[0], 0)

		processes = []
		with ThreadPoolExecutor(max_workers=15) as executor:
			 for i, profile in enumerate(profiles):
				 processes.append(executor.submit(FootLockerCreateAccount, i, profile))

		# Logger.info('Finished!')
