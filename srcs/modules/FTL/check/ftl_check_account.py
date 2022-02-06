# **************************************************************************** #
# 														   LE - /			 #
# 															   /			  #
# 	ftl_check_account.py							 .::	.:/ .	  .::	#
# 												  +:+:+   +:	+:  +:+:+	 #
# 	By: amonteli <amontelimart@gmail.com>		  +:+   +:	+:	+:+	  #
# 												  #+#   #+	#+	#+#	   #
# 	Created: 2021/02/09 10:43:37 by amonteli	 #+#   ##	##	#+#		#
# 	Updated: 2021/02/10 20:08:27 by amonteli	###	#+. /#+	###.fr	  #
# 														  /				   #
# 														 /					#
# **************************************************************************** #

import requests
import json
import random
import time

from proxy.controller import ProxyManager
from logger.logger import Logger
from logger.fileLogger import logEntry, logWaitingList
from notifier.discord import DiscordNotifier


class FootLockerCheckAccount:
	def __init__(self, index, profile):

		Logger.info(f"[{index}] Starting checking Raffle ({profile['email']})")

		self.session = requests.Session()

		self.proxy = ProxyManager().getProxy()
		self.indexProfile = index
		self.profile = profile

		self.initFTLSession()
		self.login()
		self.fetchAccountInformations()

		self.fetchReleases()

		self.initFTLSession(customHeaders=True)
		self.confirmWin()

	def initFTLSession(self, customHeaders=None):
		Logger.info(f"[{self.indexProfile}] Initing session")

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
				"https://www.footlocker.fr/apigate/session",
				headers=headers,
				proxies=self.proxy,
			)

			if "Waiting Room Page" in response.text:
				Logger.error("Queue is online! Retrying in 60's.")
				# time.sleep(60)
				return self.initFTLSession()

			if response.status_code == 403 or "url" in response.json():
				ProxyManager().banProxy(self.proxy["https"])
				self.proxy = ProxyManager().getProxy()
				Logger.error("Proxy banned. Switching proxy!")
				return self.initFTLSession()

		except Exception as e:
			Logger.error("Exception has occured, retrying getting session...")
			Logger.error(e)
			return self.initFTLSession()

		self.sessionId = response.headers.get("x-flapi-session-id")
		self.csrfToken = response.json()["data"]["csrfToken"]

		Logger.info(f"[{self.indexProfile}] Successfully fetched SessionId & CSRF!")

	def login(self):
		headers = {
			'Host': 'www.footlocker.fr',
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
				"https://www.footlocker.fr/apigate/auth",
				headers=headers,
				data=userLogin,
				proxies=self.proxy,
			)

			if response.status_code == 403 or "url" in response.json():
				Logger.error("Proxy banned. Switching proxy!")
				ProxyManager().banProxy(self.proxy["https"])
				self.proxy = ProxyManager().getProxy()
				return self.login()

			if "Waiting Room Page" in response.text:
				Logger.error("Queue is online! Retrying in 60's.")
				return self.login()


		except Exception as error:
			Logger.error("Exception has occured, AUTH")
			Logger.error(error)
			return self.login()

		print(response.json())
		self.sessionId = response.headers.get("x-flapi-session-id")
		self.accessToken = response.json()["oauthToken"]["access_token"]
		Logger.info("Successfully connected to account!")

	def fetchAccountInformations(self):
		headers = {
			'Host': 'www.footlocker.fr',
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
				"https://www.footlocker.fr/apigate/users/account-info",
				headers=headers,
				proxies=self.proxy,
			)

			if response.status_code == 403 or "url" in response.json():
				Logger.error("Proxy banned. Switching proxy!")
				ProxyManager().banProxy(self.proxy["https"])
				self.proxy = ProxyManager().getProxy()
				return self.fetchAccountInformations()

			self.name = f"{response.json()['firstName']} {response.json()['lastName']}"
			self.customerId = response.json()["customerID"]

		except Exception as error:
			Logger.error("Exception has occured, Account Fetcher")
			Logger.error(error)

	def fetchReleases(self):
		headers = {
			"Host": "www.footlocker.fr",
			"x-time-zone": "Europe/Paris",
			"x-flapi-timeout": "42898",
			"x-fl-app-version": "4.6.4",
			"x-flapi-api-identifier": "921B2b33cAfba5WWcb0bc32d5ix89c6b0f614",
			"x-flapi-session-id": self.sessionId,
			"x-flapi-resource-identifier": self.accessToken,
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
			response = self.session.get(
				"https://www.footlocker.fr/apigate/release-calendar",
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

		except Exception as error:
			# print(error)
			Logger.error("Exception has occured, retrying getting current releases...")
			# error.with_traceback()
			# return (self.fetchReleases())

		# with open('waitling.json', "w") as SettingsFile:
		# 	SettingsFile.write(json.dumps(currentReleases, indent=4))

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
					self.profile["password"],
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
				with open("wl.csv", "a") as wlFile:
					wlFile.write(
						f"{self.email},{self.password},{release['reservation']['statusCode']}"
					)

	def confirmWin(self):
		headers = {
			"Host": "www.footlocker.fr",
			"x-flapi-timeout": "42883",
			"x-flapi-session-id": self.sessionId,
			"x-fl-app-version": "4.6.4",
			"x-flapi-api-identifier": "921B2b33cAfba5WWcb0bc32d5ix89c6b0f614",
			"x-flapi-resource-identifier": self.accessToken,
			"x-fl-device-id": "68DDAFA4-5645-4525-A1B5-DD0FE0D96417",
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
			response = self.session.get(
				"https://www.footlocker.fr/apigate/session",
				headers=headers,
				proxies=self.proxy,
			)

			if response.status_code == 403 or "url" in response.json():
				Logger.error("Proxy banned. Switching proxy!")
				ProxyManager().banProxy(self.proxy["https"])
				self.proxy = ProxyManager().getProxy()
				return self.confirmWin()

		except Exception as error:
			Logger.error("Exception has occured, SESSION")
			# error.with_traceback()
			return self.confirmWin()

		self.sessionId = response.headers.get("x-flapi-session-id")
		self.csrfToken = response.json()["data"]["csrfToken"]

		headers = {
			"Host": "www.footlocker.fr",
			"x-flapi-timeout": "42882",
			"x-api-lang": "fr-FR",
			"x-flapi-resource-identifier": self.accessToken,
			"user-agent": "FLEU/CFNetwork/Darwin",
			"x-api-country": "FR",
			"x-customer-number": self.customerId,
			"x-fl-app-version": "4.6.4",
			"x-flapi-session-id": self.sessionId,
			"x-csrf-token": self.csrfToken,
			"x-fl-request-id": "68519C1A-EE4D-4112-BFC9-FB124B1709D9",
			"accept-language": "fr-FR,fr;q=0.8",
			"x-flapi-api-identifier": "921B2b33cAfba5WWcb0bc32d5ix89c6b0f614",
			"x-time-zone": "Europe/Paris",
			"content-type": "application/json",
			"x-fl-device-id": "68DDAFA4-5645-4525-A1B5-DD0FE0D96417",
			"accept": "application/json",
			"x-api-key": "DjpcK97IzdUPQGvv9rX8FEcINrbqzZRt",
			"pragma": "no-cache",
			"cache-control": "no-cache",
		}

		try:
			response = self.session.put(
				"https://www.footlocker.fr/apigate/reservations/{}/confirm".format(
					self.reservationId
				),
				headers=headers,
				proxies=self.proxy,
			)

			if response.status_code == 403 or "url" in response.json():
				Logger.error("Proxy banned. Switching proxy!")
				ProxyManager().banProxy(self.proxy["https"])
				self.proxy = ProxyManager().getProxy()
				return self.confirmWin()

		except Exception as error:
			Logger.error("Exception has occured, retrying getting current releases...")
			error.with_traceback()
			return self.confirmWin()

		# print(response.text)
		# print(response.status_code)
		# print(response.json())

		if response.status_code == 200:
			DiscordNotifier.winned(
				self.profile["email"],
				self.name,
				self.profile["password"],
				shop=self.winnerShopName,
				img=self.imgUrl,
			)
