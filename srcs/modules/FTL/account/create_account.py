'''

[account] create_account.py

Author: seith <seith.corp@gmail.com>

Created: 01/03/2021 14:54:32 by seith
Updated: 01/03/2021 14:54:32 by seith

Synezia Corp. (c) 2021 - MIT

'''

import requests
import json
import random

from utils.cli_utils import printHeader, printLine
from logger.logger import Logger
from proxy.controller import ProxyManager
from controller.profile_parser import fetchProfiles

from modules.FootLockerMerde.ftl_utils import get_random_date

class CreateAccount():

	def __init__(self, index, profile):
		Logger.info(f"[{index}] Creating {profile['email']}")

		self.session = requests.Session()

		self.proxy = ProxyManager().getProxy()
		self.profile = profile
		self.index = index

		self.regionCode = 'BE'

		self.initSession()
		self.createAccount()

	def initSession(self):
		headers = {
			'Host': 'www.footlocker.be',
			'accept': 'application/json',
			'x-fl-app-version': '4.7.1',
			'x-flapi-api-identifier': '921B2b33cAfba5WWcb0bc32d5ix89c6b0f614',
			'x-fl-device-id': '68DDAFA4-5645-4525-A1B5-DD0FE0D96417',
			'accept-language': 'fr-FR,fr;q=0.8',
			'x-api-key': 'EQJstIXfZDXXwwuGYdXr5rHNUyZtA3Jk',
			'user-agent': 'FLEU/CFNetwork/Darwin',
			'x-api-country': self.regionCode,
			'x-api-lang': 'fr-FR',
			'pragma': 'no-cache',
			'cache-control': 'no-cache',
		}

		try:
			response = self.session.get(
				"https://www.footlocker.be/apigate/session",
				headers=headers,
				proxies=self.proxy,
			)

			if "Waiting Room Page" in response.text:
				Logger.error("Queue is online! Retrying in 60's.")
				time.sleep(60)
				return self.initSession()

			if response.status_code == 403 or "url" in response.json():
				ProxyManager().banProxy(self.proxy["https"])
				self.proxy = ProxyManager().getProxy()
				return self.initSession()

		except Exception as e:
			Logger.error("Exception has occured, retrying getting session...")
			Logger.error(e)
			ProxyManager().banProxy(self.proxy["https"])
			self.proxy = ProxyManager().getProxy()
			return self.initSession()

		self.sessionId = response.headers.get("x-flapi-session-id")
		self.csrfToken = response.json()["data"]["csrfToken"]

	def createAccount(self):
		headers = {
			'Host': 'www.footlocker.be',
			'content-type': 'application/json',
			'accept': 'application/json',
			"x-flapi-session-id": self.sessionId,
			'x-fl-app-version': '4.7.1',
			'x-flapi-api-identifier': '921B2b33cAfba5WWcb0bc32d5ix89c6b0f614',
			'x-fl-device-id': '68DDAFA4-5645-4525-A1B5-DD0FE0D96417',
			'accept-language': 'fr-FR,fr;q=0.8',
			'x-api-key': 'EQJstIXfZDXXwwuGYdXr5rHNUyZtA3Jk',
			'user-agent': 'FLEU/CFNetwork/Darwin',
		    'x-api-country': self.regionCode,
			'x-api-lang': 'fr-FR',
			"x-csrf-token": self.csrfToken,
			'x-fl-request-id': 'E8BBDC71-9302-49BD-8E7B-2AF39CFC6CBB',
			'pragma': 'no-cache',
			'cache-control': 'no-cache',
		}

		accountProfile = {
			"birthday": get_random_date(),
			"firstName": self.profile["first_name"],
			"preferredLanguage": "fr",
			"lastName": self.profile["last_name"],
			"uid": self.profile["email"],
			"password": self.profile["password"],
		}

		userRegister = json.dumps(accountProfile, separators=(",", ":"))

		try:		
			response = self.session.post(
				"https://www.footlocker.be/apigate/users",
				headers=headers,
				data=userRegister,
				proxies=self.proxy,
			)

			if response.status_code == 403:
				ProxyManager().banProxy(self.proxy["https"])
				self.proxy = ProxyManager().getProxy()
				return self.createAccount()

		except Exception as error:
			Logger.error("Exception has occured when creating account...")
			Logger.error(error)
			ProxyManager().banProxy(self.proxy["https"])
			self.proxy = ProxyManager().getProxy()
			f = open('logs/dieg_ftl_account_create.csv', 'a')
			f.write(f"FAILED,{self.profile['first_name']},{self.profile['last_name']},{self.profile['email']},{self.profile['password']}\n")
			f.close()
			return

		if (response.status_code == 201):
			f = open('logs/dieg_ftl_account_create.csv', 'a')
			f.write(f"CREATED,{self.profile['first_name']},{self.profile['last_name']},{self.profile['email']},{self.profile['password']}\n")
			f.close()
			Logger.success(f"Successfully created {self.profile['email']}")
			return 

		if ("BackendExceptionError" in response.text):
			# Logger.error(f"[{self.index}] {self.profile['email']} failed backend seems dead.")
			return self.createAccount()
		
		if ("finaliser" in response.text):
			Logger.error('Already registered')
			f = open('logs/dieg_ftl_account_create.csv', 'a')
			f.write(f"REGISTERED,{self.profile['first_name']},{self.profile['last_name']},{self.profile['email']},{self.profile['password']}\n")
			f.close()
			return 
			
		f = open('logs/dieg_ftl_account_create.csv', 'a')
		f.write(f"FAILED,{self.profile['first_name']},{self.profile['last_name']},{self.profile['email']},{self.profile['password']}\n")
		f.close()