"""

[checker] ftl_checker_module.py

Author: seith <seith.corp@gmail.com>

Created: 09/02/2021 19:55:07 by seith
Updated: 09/02/2021 19:55:07 by seith

Synezia Corp. (c) 2021 - MIT

"""

import requests
import json
import inquirer
import glob
import random

from utils.cli_utils import printHeader, printLine
from logger.logger import Logger
from proxy.controller import ProxyManager
from controller.profile_parser import fetchProfiles
from .ftl_check_account import FootLockerCheckAccount

from concurrent.futures import ThreadPoolExecutor, as_completed


class FootLockerCheckerModule:
    def __init__(self):

        self.session = requests.Session()

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

        # for i, profile in enumerate(profiles):
        # FootLockerCheckAccount(i, profile)
        # FootLockerCheckAccount()

        processes = []
        with ThreadPoolExecutor(max_workers=100) as executor:
            for i, profile in enumerate(profiles):
                processes.append(executor.submit(FootLockerCheckAccount, i, profile))

        # Logger.info('Finished!')
