'''

[account] account_module.py

Author: seith <seith.corp@gmail.com>

Created: 15/03/2021 21:27:46 by seith
Updated: 15/03/2021 21:27:46 by seith

Synezia Corp. (c) 2021 - MIT

'''

import os

from concurrent.futures import ThreadPoolExecutor, as_completed

from singleton import Instance
from profiles import Profile

from proxy.controller import ProxyManager
from utils.colors import Color
from logger.logger import Logger

from .create_account import CreateAccount

from configuration.configuration import Configuration

class AccountModule():

	def __init__(self):

		Instance().updateRPC("Generating FootLocker accounts..")
		
		version = "0.0.1-BETA"
		moduleName = "FootLocker"
		action = "Account_Create"
		date = Instance().getDate()
		loggerFileName = f"logs/{moduleName}/{action}_{date}.csv"

		""" Proxy """
		
		if (not Configuration().proxyless):
			self.proxyManager = ProxyManager(moduleName)
			self.proxy = self.proxyManager.getProxy()
		else:
			Logger.info('Using Mode: Proxyless if you dont want that please edit settings/settings.json!')

		""" Profiles """

		profile = Profile(moduleName)
		self.profiles = profile.fetchProfiles()

		""" Create Logger """

		try:
			f = open(loggerFileName, 'a')
			f.write(f"status,first_name,last_name,email,password,country\n")
			f.close()
		except Exception as error:
			Logger.error(error)

		with ThreadPoolExecutor(max_workers=100) as executor:
			for index, profile in enumerate(self.profiles):
				if (not 'country' in profile or not profile['country']):
					profile['country'] = 'fr'
				executor.submit(CreateAccount, index, profile, loggerFileName)

		input("Close CLI? Press Enter")