'''

[raffle] enter_raffle.py

Author: seith <seith.corp@gmail.com>

Created: 12/04/2021 12:36:13 by seith
Updated: 12/04/2021 12:36:13 by seith

Synezia Corp. (c) 2021 - MIT

'''

import requests
import json
import random
import time

from logger.logger import Logger

from proxy.controller import ProxyManager

from logger.fileLogger import logEntry, logWaitingList
from notifier.discord import DiscordNotifier

class FootLockerEnterRaffle():

	def __init__(self, index, profile, sizes, stores, productId):
		Logger.info(f"[{index}] Starting Task for [{profile['email']}")

		self.index = index
		self.profile = profile
		self.sizes = sizes
		self.stores = stores 
		self.productId = productId

		self.proxy = ProxyManager().getProxy()

		if ("None" in profile['sessionId']):
			return 

		""" Exec """
		# self.initSession()
		# print(f"csrf={self.csrfToken}")
		# print(f"sessionId={self.sessionId}")

		# if ("sessionId" in profile)

		# self.login()
		self.getCustomerId()
		self.fetchReleases()
		# self.enterRaffle()

	def initSession(self):
		Logger.info(f"[{self.index}] Initing Session...")

		headers = {
			'user-agent': 'FLEU/CFNetwork/Darwin',
		}

		try:
			response = requests.get('https://www.footlocker.fr/apigate/session', headers=headers, allow_redirects=False, proxies=self.proxy)
		except requests.exceptions.ProxyError:
			Logger.error(f"[{self.index}] Proxy Error. Rotating proxy...")
			ProxyManager().banProxy(self.proxy["https"])
			self.proxy = ProxyManager().getProxy()

		except Exception as error:
			Logger.error(f"[{self.index}] {error}")

		if "Waiting Room Page" in response.text:
			Logger.error(f"[{self.index}] Queue UP")
			time.sleep(60)
			return self.initSession()

		if response.status_code == 403 or "url" in response.json():
			Logger.error(f"[{self.index}] Proxy Ban. Rotating Proxy...")
			ProxyManager().banProxy(self.proxy["https"])
			self.proxy = ProxyManager().getProxy()
			return self.initSession()

		self.sessionId = response.headers.get("x-flapi-session-id")
		self.csrfToken = response.json()["data"]["csrfToken"]

	def login(self):

		Logger.info(f"[{self.index}] Starting Login...")
		headers = {
			'Host': 'www.footlocker.fr',
			'content-type': 'application/json',
			'accept': 'application/json',
			'x-flapi-session-id': self.sessionId,
			'x-fl-app-version': '4.8.0',
			'x-flapi-api-identifier': '921B2b33cAfba5WWcb0bc32d5ix89c6b0f614',
			'x-fl-device-id': '68DDAFA4-5645-4525-A1B5-DD0FE0D96417',
			'accept-language': 'fr-FR,fr;q=0.8',
			'x-api-key': 'DjpcK97IzdUPQGvv9rX8FEcINrwqzZRt',
			'user-agent': 'FLEU/CFNetwork/Darwin',
			'x-api-country': 'FR',
			'x-api-lang': 'fr-FR',
			'x-csrf-token': self.csrfToken,
			'x-newrelic-id': 'VgAPVVdRDRAIV1lXAAEEXlQ=',
			'x-fl-request-id': '2A5C50B0-BB3A-4D7E-8564-9BAC5B74E64B',
			'pragma': 'no-cache',
			'cache-control': 'no-cache',
		}

		accountProfile = {
			"uid": self.profile["email"],
			"password": self.profile["password"],
		}

		userLogin = json.dumps(accountProfile, separators=(",", ":"))

		while True:
			response = requests.post('https://www.footlocker.fr/api/auth', headers=headers, data=userLogin, proxies=self.proxy)
			print(response.text)
			print(response.status_code)

			# Logger.error(f"[{self.index}] Proxy Ban. Rotating Proxy...")
			ProxyManager().banProxy(self.proxy["https"])
			self.proxy = ProxyManager().getProxy()

			if (response.status_code == 400):
				break

	def getCustomerId(self):
		headers = {
			'Host': 'www.footlocker.be',
			'x-fl-request-id': '4A51C6ED-B95E-4CD2-9902-C266FF66E9A6',
			'x-flapi-timeout': '31115',
			'x-flapi-session-id': self.profile['sessionId'],
			'x-fl-app-version': '4.8.0',
			'x-flapi-api-identifier': '921B2b33cAfba5WWcb0bc32d5ix89c6b0f614',
			'x-flapi-resource-identifier': self.profile['accessToken'],
			'x-fl-device-id': '68DDAFA4-5645-4525-A1B5-DD0FE0D96417',
			'accept': 'application/json',
			'accept-language': 'fr-FR,fr;q=0.8',
			'x-api-key': 'DjpcK97IzdUPQGvv9rX8FEcINrbqzZRt',
			'user-agent': 'FLEU/CFNetwork/Darwin',
			'x-api-country': 'FR',
			'x-api-lang': 'fr-FR',
			'x-newrelic-id': 'VgAPVVdRDRAIV1lXAAEEXlQ=',
			'pragma': 'no-cache',
			'cache-control': 'no-cache',
		}

		try:
			response = requests.get('https://www.footlocker.be/apigate/users/account-info', headers=headers)

			print(response.json()['customerID'])
			self.name = f"FDP"
			self.customerId = response.json()['customerID']
			self.email = self.profile['email']
		except Exception as error:
			Logger.error(f"{error}")

				
	def getCSRF(self):
		headers = {"user-agent": "FLEU/CFNetwork/Darwin"}

		response = requests.get(
			"https://www.footlocker.be/apigate/session",
			headers=headers,
		)

		csrfToken = response.json()["data"]["csrfToken"]

		return csrfToken

	
	def prepareEnterParams(self):
		size = random.choice(self.sizes)
		storeIds = list()

		for store in self.stores:
			storeIds.append(store)

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
			"x-flapi-resource-identifier": self.profile['accessToken'],
			'user-agent': 'FLEU/CFNetwork/Darwin',
			'x-api-country': 'BE',
			"x-customer-number": self.customerId,
			'x-fl-app-version': '4.7.1',
			"x-flapi-session-id": self.profile['sessionId'],
			"x-csrf-token": self.getCSRF(),
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
			response = requests.post(
				"https://www.footlocker.be/apigate/reservations/",
				headers=headers,
				data=self.prepareEnterParams(),
				allow_redirects = False
			)

		except Exception as error:
			if response.status_code == 503:
				Logger.error("Server FTL is dead.")
				return
			Logger.error(error)
			return

		if response.status_code == 201:
			Logger.success(
				f"[{self.index}] Successfully entered into Raffle ({self.profile['email']})"
			)
			# logEntry(self.profile["email"], self.profile["password"])
			return

		if response.json() and response.json()["errors"]:
			# print(response.text)
			Logger.error(
				f"[{self.index}] {response.json()['errors'][0]['subject']} on {self.profile['email']}"
			)
			return "Error"

	def fetchReleases(self):
		headers = {
			"Host": "www.footlocker.fr",
			"x-time-zone": "Europe/Paris",
			"x-flapi-timeout": "42898",
			"x-fl-app-version": "4.6.4",
			"x-flapi-api-identifier": "921B2b33cAfba5WWcb0bc32d5ix89c6b0f614",
			"x-flapi-session-id": self.profile['sessionId'],
			"x-flapi-resource-identifier": self.profile['accessToken'],
			"x-fl-device-id": "68DDAFA4-5645-4525-A1B5-DD0FE0D96417",
			"x-customer-number": self.customerId,
			"accept": "application/json",
			"accept-language": "fr-FR,fr;q=0.8",
			"x-api-key": "DjpcK97IzdUPQGvv9rX8FEcINrbqzZRt",
			"user-agent": "FLEU/CFNetwork/Darwin",
			"x-api-country": "BE",
			"x-api-lang": "fr-FR",
			"pragma": "no-cache",
			"cache-control": "no-cache",
		}

		try:
			response = requests.get(
				"https://www.footlocker.be/apigate/release-calendar",
				headers=headers,
				proxies=self.proxy,
			)

			# print(response.text)

			if response.status_code == 403 or "url" in response.json():
				Logger.error("Proxy banned. Switching proxy!")
				ProxyManager().banProxy(self.proxy["https"])
				self.proxy = ProxyManager().getProxy()
				return self.fetchReleases()

			if "Waiting Room Page" in response.text:
				Logger.error("Queue is online! Retrying in 60's.")
				# time.sleep(60)
				return self.fetchReleases()

			releases = response.json()["releaseCalendarProducts"]
			releaseReservation = [x for x in releases if "reservation" in x]
			currentReleases = [
				x for x in releaseReservation if x["reservation"]["statusCode"] > 0
			]

			print(currentReleases)

			# print

		except Exception as error:
			# print(error)
			Logger.error("Exception has occured, retrying getting current releases...")
			# error.with_traceback()
			# return (self.fetchReleases())

		with open('waitling.json', "w") as SettingsFile:
			SettingsFile.write(json.dumps(response.json(), indent=4))

		for release in currentReleases:
			if release["reservation"]["statusCode"] == 6:  # WINNED = 6
				self.reservationId = release["reservation"]["reservationId"]
				self.imgUrl = release["image"]

				self.winnerShopId = release["reservation"]["pickupStoreId"]

				for shop in release["reservation"]["selectedStores"]:
					if shop["id"] == self.winnerShopId:
						self.winnerShopName = shop["displayName"]

				Logger.success(
					f"[WIN] Win found for {self.name} with {self.profile['email']} at {self.winnerShopName}"
				)
				DiscordNotifier.foundWin(
					self.profile["email"],
					self.name,
					"Motdepasse456!",
					shop=self.winnerShopName,
					img=self.imgUrl,
				)
				Logger.info('Confirming ...')
				# self.confirmWin()

			if release["reservation"]["statusCode"] == 5:
				Logger.success(
					f"[WaitingList] Waiting List for {self.name}, {self.profile['email']}"
				)
				with open("wl.csv", "a") as wlFile:
					wlFile.write(f"{self.email},{self.password}")

			else:
				Logger.error(f"Didn't win...")
