"""

[FootLocker] ftl_enter_raffle.py

Author: seith <seith.corp@gmail.com>

Created: 07/02/2021 21:25:59 by seith
Updated: 07/02/2021 21:25:59 by seith

Synezia Corp. (c) 2021 - MIT

"""

import requests
import json
import random

from proxy.controller import ProxyManager
from logger.logger import Logger
from logger.fileLogger import logEntry


class FootLockerEnterAccount:
	def __init__(self, profile, sizes, stores, productId, index):
		Logger.info(f"[{index}] Starting entering into Raffle ({profile['email']})")

		self.session = requests.Session()

		self.proxy = ProxyManager().getProxy()
		self.profile = profile
		self.sizes = sizes
		self.stores = stores
		self.productId = productId
		self.indexProfile = index

		# Init FTL Session
		self.initFTLSession()
		self.login()
		self.fetchAccountInformations()
		self.initFTLSession("yes")
		self.enterRaffle()

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
				"https://www.footlocker.be/apigate/session",
				headers=headers,
				proxies=self.proxy,
				allow_redirects = False
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
			return 

		self.sessionId = response.headers.get("x-flapi-session-id")
		self.csrfToken = response.json()["data"]["csrfToken"]

		# Logger.info('Successfully fetched SessionId & CSRF!')

	def login(self):
		headers = {
			'Host': 'www.footlocker.be',
			'content-type': 'application/json',
			'accept': 'application/json',
			'x-flapi-session-id': self.sessionId,
			'x-fl-app-version': '4.7.1',
			'x-flapi-api-identifier': '921B2b33cAfba5WWcb0bc32d5ix89c6b0f614',
			'x-fl-device-id': '68DDAFA4-5645-4525-A1B5-DD0FE0D96417',
			'accept-language': 'fr-FR,fr;q=0.8',
			'x-api-key': 'EQJstIXfZDXXwwuGYdXr5rHNUyZtA3Jk',
			'user-agent': 'FLEU/CFNetwork/Darwin',
			'x-api-country': 'BE',
			'x-api-lang': 'fr-FR',
			'x-csrf-token': self.csrfToken,
			'x-fl-request-id': 'AC928121-6965-4BA3-9B25-289A54C08653',
			'pragma': 'no-cache',
			'cache-control': 'no-cache',
		}

		accountProfile = {
			"uid": self.profile["email"],
			"password": self.profile["password"],
		}

		userLogin = json.dumps(accountProfile, separators=(",", ":"))

		try:
			response = self.session.post(
				"https://www.footlocker.be/apigate/auth",
				headers=headers,
				data=userLogin,
				proxies=self.proxy,
				allow_redirects = False
			)

			if response.status_code == 403 or "url" in response.json():
				# Logger.error('Proxy banned. Switching proxy!')
				ProxyManager().banProxy(self.proxy["https"])
				self.proxy = ProxyManager().getProxy()
				return self.login()

			if ("Backend seem unreachable" in response.text):
				Logger.error('FTL Server are dead. (Backend seem unreachable.)')
				return

			# print(response.text)

			self.sessionId = response.headers.get("x-flapi-session-id")
			self.accessToken = response.json()["oauthToken"]["access_token"]

		except Exception as error:
			Logger.error("Exception has occured, failed to logged-in")
			Logger.error(error)
			error.with_traceback(self)
			return self.login()

		Logger.info('Successfully connected to account!')

	def fetchAccountInformations(self):

		headers = {
			'Host': 'www.footlocker.be',
			"x-flapi-session-id": self.sessionId,
			'x-fl-app-version': '4.7.1',
			'x-flapi-api-identifier': '921B2b33cAfba5WWcb0bc32d5ix89c6b0f614',
			'x-flapi-resource-identifier':  self.accessToken,
			'x-fl-device-id': '68DDAFA4-5645-4525-A1B5-DD0FE0D96417',
			'accept': 'application/json',
			'accept-language': 'fr-FR,fr;q=0.8',
			'x-api-key': 'EQJstIXfZDXXwwuGYdXr5rHNUyZtA3Jk',
			'user-agent': 'FLEU/CFNetwork/Darwin',
			'x-api-country': 'BE',
			'x-api-lang': 'fr-FR',
			'pragma': 'no-cache',
			'cache-control': 'no-cache',
		}

		try:
			response = self.session.get(
				"https://www.footlocker.be/apigate/users/account-info",
				headers=headers,
				proxies=self.proxy,
				allow_redirects = False
			)

			if response.status_code == 403 or "url" in response.json():
				# Logger.error('Proxy banned. Switching proxy!')
				ProxyManager().banProxy(self.proxy["https"])
				self.proxy = ProxyManager().getProxy()
				return self.fetchAccountInformations()

			self.customerId = response.json()["customerID"]

		except Exception as error:
			Logger.error("Exception has occured, retrying getting current releases...")
			error.with_traceback()
			ProxyManager().banProxy(self.proxy["https"])
			self.proxy = ProxyManager().getProxy()
			return self.fetchAccountInformations()

		Logger.info('Successfully fetched account!')

	def prepareEnterParams(self):
		size = random.choice(self.sizes)
		storeIds = list()

		for store in self.stores:
			storeIds.append(store["id"])

		globalData = {}
		globalData["data"] = {}

		mySize = {
			"us": size["us"],
			"selectedRegion": "eu",
			"uk": size["uk"],
			"eu": size["eu"],
		}

		globalData["data"]["attributes"] = {
			"storeIds": storeIds,
			"size": mySize,
			"launchEventId": self.productId,
			"platform": "ios",
		}

		globalData["type"] = "reservation"
		return json.dumps(globalData, separators=(",", ":"))

	def enterRaffle(self):
		headers = {
			'Host': 'www.footlocker.be',
			'x-flapi-timeout': '42853',
			'x-api-lang': 'fr-FR',
			"x-flapi-resource-identifier": self.accessToken,
			'user-agent': 'FLEU/CFNetwork/Darwin',
			'x-api-country': 'BE',
			"x-customer-number": self.customerId,
			'x-fl-app-version': '4.7.1',
			"x-flapi-session-id": self.sessionId,
			"x-csrf-token": self.csrfToken,
			'x-fl-request-id': 'D25B980E-5A92-4D2B-BB71-B14ACF93F66B',
			'accept-language': 'fr-FR,fr;q=0.8',
			'x-flapi-api-identifier': '921B2b33cAfba5WWcb0bc32d5ix89c6b0f614',
			'x-time-zone': 'Europe/Paris',
			'content-type': 'application/json',
			'x-fl-device-id': '68DDAFA4-5645-4525-A1B5-DD0FE0D96417',
			'accept': 'application/json',
			'x-api-key': 'EQJstIXfZDXXwwuGYdXr5rHNUyZtA3Jk',
			'pragma': 'no-cache',
			'cache-control': 'no-cache',
		}

		try:
			response = self.session.post(
				"https://www.footlocker.be/apigate/reservations/",
				headers=headers,
				data=self.prepareEnterParams(),
				proxies=self.proxy,
				allow_redirects = False
			)

			if response.status_code == 403 or "url" in response.json():
				# Logger.error('Proxy banned. S\witching proxy!')
				ProxyManager().banProxy(self.proxy["https"])
				self.proxy = ProxyManager().getProxy()
				return self.enterRaffle()

		except Exception as error:
			if response.status_code == 503:
				Logger.error("Server FTL is dead.")
				return
			Logger.error(error)
			return

		if response.status_code == 201:
			Logger.success(
				f"[{self.indexProfile}] Successfully entered into Raffle ({self.profile['email']})"
			)
			logEntry(self.profile["email"], self.profile["password"])
			return

		if response.json() and response.json()["errors"]:
			# print(response.text)
			Logger.error(
				f"[{self.indexProfile}] {response.json()['errors'][0]['subject']} on {self.profile['email']}"
			)
			return "Error"
