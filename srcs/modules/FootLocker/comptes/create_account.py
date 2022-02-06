'''

[account] create_account.py

Author: seith <seith.corp@gmail.com>

Created: 03/04/2021 18:09:03 by seith
Updated: 03/04/2021 18:09:03 by seith

Synezia Corp. (c) 2021 - MIT

'''


import requests
import random
import json
import datetime
import time

from proxy.controller import ProxyManager
from logger.logger import Logger
from configuration.configuration import Configuration

def get_random_date():
	try:
		date = datetime.datetime.strptime('{} {}'.format(random.randint(1, 366), random.randint(1990, 2003)), '%j %Y')
		dateSplit = str(date).split(' ')[0]

		parsed = dateSplit.split('-')
		text = parsed[1] + '/' + parsed[2] + '/' + parsed[0]

		return text
	except ValueError:
		get_random_date()

class CreateAccount():

	def __init__(self, index, profile, loggerFileName, userAgent):
		Logger.info(f"[{index}] Creating {profile['email']}...")

		""" Values """
		self.index = index
		self.profile = profile
		self.loggerFileName = loggerFileName
		self.userAgent = userAgent

		self.success = False
		if (not Configuration().proxyless):
			self.proxy = ProxyManager().getProxy()
		self.retry = 0

		""" Task """
		accountStatus: int = self.createAccount()

		if (accountStatus == 1):
			Logger.success(f"[{self.index}] Successfully registered {self.profile['email']}!")
			self.success = True
			self.state = "CREATED"
		elif (accountStatus == 2):
			Logger.warning(f"[{self.index}] Already registered {self.profile['email']}!")
			self.success = True
			self.state = "REGISTERED"
		else:
			self.state = "FAILED"
			self.success = False
			Logger.error(f"[{self.index}] Failed to register {self.profile['email']}")

	def createAccount(self):
		headers = {
			'user-agent': self.userAgent,
		}

		registerData = {
			"bannerEmailOptIn": "false",
			"termsAndCondition": "true",
			"firstName": self.profile['first_name'],
			"lastName": self.profile['last_name'],
			"postalCode": "75005",
			"uid": self.profile['email'],
			"phoneNumber": "0653131445",
			"birthday": get_random_date(),
			"gender": "male",
			"password": self.profile['password'],
			"preferredLanguage": "en",
			"loyaltyStatus": "true",
			"wantToBeVip": "false",
			"flxTcVersion": "1.0",
			"loyaltyFlxEmailOptIn": "true"
		}

		registerData["country"] = {
			"isocode": "FR",
			"name": "France"
		}

		data = json.dumps(registerData, separators=(",", ":"))

		while True:

			try:
				if (Configuration().proxyless):
					response = requests.post('https://www.footlocker.fr/api/v2/users', headers=headers, data=data)
				else:
					response = requests.post('https://www.footlocker.fr/api/v2/users', headers=headers, data=data, proxies=ProxyManager().getProxy())

			except Exception as error:
				if (Configuration().proxyless):
					Logger.error(f"[{self.index}] You ip was banned... Please use Proxies Mode! ")
					time.sleep(60)
					return

				if (self.retry > 15):
					return -1

				if (self.retry > 5):
					if (not Configuration().proxyless):
						ProxyManager().banProxy(self.proxy["https"])
						self.proxy = ProxyManager().getProxy()
						Logger.error(f"[{self.index}] Proxy Banned. Rotating proxy...")
				else:
					Logger.error(f"[{self.index}] Unknown error. Maybe ClownLocker server. Retrying")

			if (response.status_code == 403):
				if (Configuration().proxyless):
					Logger.error(f"[{self.index}] You ip was banned... Please use Proxies Mode! ")
					time.sleep(60)
					return
				else:
					ProxyManager().banProxy(self.proxy["https"])
					self.proxy = ProxyManager().getProxy()
				
			if (response.status_code == 201):
				return 1

			if ("Account creation has already begun" in response.text):
				return 2