'''

[account] ftl_create_account.py

Author: seith <seith.corp@gmail.com>

Created: 15/02/2021 22:32:33 by seith
Updated: 15/02/2021 22:32:33 by seith

Synezia Corp. (c) 2021 - MIT

'''


import requests
import json
import random

from proxy.controller import ProxyManager
from logger.logger import Logger
from logger.fileLogger import logEntry
from modules.FootLocker.ftl_utils import get_random_date

class FootLockerCreateAccount:
	def __init__(self, index, profile):
		Logger.info(f"[{index}] Starting creating ({profile['email']})")

		self.session = requests.Session()

		self.proxy = ProxyManager().getProxy()
		self.profile = profile
		self.indexProfile = index

		# Init FTL Session
		self.initFTLSession()
		self.createAccount()

	def initFTLSession(self, customHeaders=None):
		# Logger.info('Initing session')

		if customHeaders is None:
			headers = {"user-agent": "FLEU/CFNetwork/Darwin"}
		else:
			headers = {
				"user-agent": "FLEU/CFNetwork/Darwin",
				"x-flapi-resource-identifier": self.accessToken,
				"x-flapi-session-id": self.sessionId,
			}

		try:
			response = self.session.get(
				"https://www.footlocker.eu/api/session",
				headers=headers,
				proxies=self.proxy,
			)

			if "Waiting Room Page" in response.text:
				Logger.error("Queue is online! Retrying in 60's.")
				time.sleep(60)
				return self.initFTLSession()

			if response.status_code == 403 or "url" in response.json():
				ProxyManager().banProxy(self.proxy["https"])
				self.proxy = ProxyManager().getProxy()
				# Logger.error('Proxy banned. Switching proxy!')
				return self.initFTLSession()

		except Exception as e:
			Logger.error("Exception has occured, retrying getting session...")
			Logger.error(e)
			return self.initFTLSession()

		self.sessionId = response.headers.get("x-flapi-session-id")
		self.csrfToken = response.json()["data"]["csrfToken"]

	def createAccount(self):
		headers = {
			"Host": "www.footlocker.eu",
			"content-type": "application/json",
			"accept": "application/json",
			"x-flapi-session-id": self.sessionId,
			"x-flapi-api-identifier": "921B2b33cAfba5WWcb0bc32d5ix89c6b0f614",
			"accept-language": "fr-FR,fr;q=0.8",
			"x-api-key": "DjpcK97IzdUPQGvv9rX8FEcINrbqzZRt",
			"user-agent": "FLEU/CFNetwork/Darwin",
		    'x-api-country': 'FR',
			"x-csrf-token": self.csrfToken,
			'x-api-lang': 'fr-FR'
		}

		accountProfile = {
			"birthday": get_random_date(),
			"firstName": self.profile["first_name"],
			"country": "FR",
			"lastName": self.profile["last_name"],
			"gender": "m",
			"uid": self.profile["email"],
			"password": self.profile["password"],
		}

		userRegister = json.dumps(accountProfile, separators=(",", ":"))

		try:		
			response = self.session.post(
				"https://www.footlocker.eu/api/users",
				headers=headers,
				data=userRegister,
				proxies=self.proxy,
			)

			if response.status_code == 403:
				# Logger.error('Proxy banned. Switching proxy!')
				ProxyManager().banProxy(self.proxy["https"])
				self.proxy = ProxyManager().getProxy()
				return self.createAccount()

		except Exception as error:
			Logger.error("Exception has occured when creating account...")
			Logger.error(error)
		
		if (response.status_code == 201):
			f = open('logs/ftl_account_create.csv', 'a')
			f.write(f"CREATED,{self.profile['first_name']},{self.profile['last_name']},{self.profile['email']},{self.profile['password']}\n")
			f.close()
			Logger.success(f"Successfully created {self.profile['email']}")
			return 

		else:
			f = open('logs/ftl_account_create.csv', 'a')
			f.write(f"FAILED,{self.profile['first_name']},{self.profile['last_name']},{self.profile['email']},{self.profile['password']}\n")
			f.close()