"""

[FootLocker] ftl_raffles_module.py

Author: seith <seith.corp@gmail.com>

Created: 07/02/2021 21:19:53 by seith
Updated: 07/02/2021 21:19:53 by seith

Synezia Corp. (c) 2021 - MIT

"""

import inquirer
import requests
import json
import time

from utils.cli_utils import printHeader, printLine
from logger.logger import Logger
from proxy.controller import ProxyManager
from controller.profile_parser import fetchProfiles
from concurrent.futures import ThreadPoolExecutor, as_completed
from .ftl_enter_raffle import FootLockerEnterAccount

from configuration.configuration import Configuration

"""
	here is the module called after user selecting action to do
	this class manage thread and other things.
	need to create a Class only doing Threading purpose and Enter.
"""


class FootLockerRaffleModule:
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

		self.promptSettings()

		"""
			UI
		"""

		printHeader()
		printLine()

		"""
			HELLO MULTITHREADING
		"""

		processes = []
		with ThreadPoolExecutor(max_workers=self.threadsNumber) as executor:
			for i, profile in enumerate(profiles):
				processes.append(
					executor.submit(
						FootLockerEnterAccount,
						profile,
						self.sizes,
						self.shops,
						self.releases["pid"],
						i,
					)
				)

		Logger.info("Finished!")

	"""
		promptSettings
	"""

	def promptSettings(self):
		self.releases = self.promptReleases()
		self.shops = self.selectShops()
		self.sizes = self.selectSizes(self.releases["sizes"])
		self.threadsNumber = self.promptThreadsNumber()

	def promptThreadsNumber(self):

		questions = [inquirer.Text("choice", message="Thread number", default="40")]

		answer = inquirer.prompt(questions).get("choice").strip()

		try:
			threads = int(answer)
		except Exception as error:
			Logger.error(
				"Check your response, threads number need to be a Integer between 1-300"
			)
			return self.promptThreadsNumber()

		if threads < 1:
			Logger.error(
				"Check your response, threads number need to be a Integer between 1-300"
			)
			return self.promptThreadsNumber()

		return threads

	"""
		initSession
	"""

	def initFTLSession(self):
		Logger.info("Initing session")

		headers = {"user-agent": "FLEU/CFNetwork/Darwin"}

		try:
			response = requests.get(
				"https://www.footlocker.eu/api/session",
				headers=headers,
				proxies=self.proxy,
			)

			if "Waiting Room Page" in response.text:
				Logger.error("Queue is online! Retrying in 60's.")
				time.sleep(60)
				return self.initFTLSession()

			if response.status_code == 403 or "url" in response.json():
				self.proxyManager.banProxy(self.proxy["https"])
				self.proxy = self.proxyManager.getProxy()
				Logger.error("Proxy banned. Switching proxy!")
				return self.initFTLSession()

		except Exception as e:
			Logger.error("Exception has occured, retrying getting session...")
			e.with_traceback()
			return self.initFTLSession()

		self.sessionId = response.headers.get("x-flapi-session-id")
		self.csrfToken = response.json()["data"]["csrfToken"]

		Logger.info("Successfully fetched SessionId & CSRF!")

	"""
		selectCurrentRelease
	"""

	def promptReleases(self):
		headers = {
			"user-agent": "FLEU/CFNetwork/Darwin",
		}

		try:
			response = requests.get(
				"https://www.footlocker.eu/api/session",
				headers=headers,
				proxies=self.proxy,
			)

		except Exception as error:
			Logger.error(error)

		if "Waiting Room Page" in response.text:
			Logger.error("Queue is online! Retrying in 60's.")
			time.sleep(60)
			return self.promptReleases()

		if response.status_code == 403 or "url" in response.json():
			self.proxyManager.banProxy(self.proxy["https"])
			self.proxy = self.proxyManager.getProxy()
			Logger.error("Proxy banned. Switching proxy!")
			return self.promptReleases()

		self.sessionId = response.headers.get("x-flapi-session-id")
		self.csrfToken = response.json()["data"]["csrfToken"]

		headers = {
			"Host": "www.footlocker.eu",
			"x-time-zone": "Europe/Paris",
			"x-fl-app-version": "4.6.4",
			"x-flapi-api-identifier": "921B2b33cAfba5WWcb0bc32d5ix89c6b0f614",
			"x-fl-device-id": "68DDAFA4-5645-4525-A1B5-DD0FE0D96417",
			"accept": "application/json",
			"accept-language": "fr-FR,fr;q=0.8",
			"x-api-key": "DjpcK97IzdUPQGvv9rX8FEcINrbqzZRt",
			"user-agent": "FLEU/CFNetwork/Darwin",
			"x-api-country": "FR",
			"x-api-lang": "fr-FR",
			"pragma": "no-cache",
			"cache-control": "no-cache",
		}

		try:
			response = requests.get(
				"https://www.footlocker.eu/api/release-calendar",
				headers=headers,
				proxies=self.proxy,
			)

			# print(response.text)
			print(self.proxy)
			releases = response.json()["releaseCalendarProducts"]
			releaseReservation = [x for x in releases if "reservation" in x]

			activeReleases = [
				x for x in releaseReservation if x["reservation"]["statusCode"] > 0
			]
		except Exception as error:
			Logger.error(error)
			ProxyManager().banProxy(self.proxy["https"])
			self.proxy = ProxyManager().getProxy()
			return self.promptReleases()

		formatedReleases = list()

		for release in activeReleases:
			payload = {
				"pid": release["reservation"]["productId"],
				"name": release["name"],
				"sizes": release["reservation"]["sizes"],
			}
			formatedReleases.append(payload)

		releasesNames = list()

		for release in formatedReleases:
			releasesNames.append(release["name"])

		questions = [
			inquirer.List(
				"choice",
				message="What raffle do you want to enter?",
				choices=releasesNames,
			),
		]

		answer = inquirer.prompt(questions).get("choice").strip()

		selectedRaffle = [x for x in formatedReleases if str(answer) in x["name"]]
		return selectedRaffle[0]

	def selectShops(self):

		"""
		UI - Prompt Address for lookin-up Shops near 160km
		"""

		questions = [
			inquirer.Text(
				"address",
				message="Please precise Location of Shops. (160km near)",
				default="Paris",
			)
		]

		addy = inquirer.prompt(questions).get("address").strip()

		"""
			fetchShops by Address
		"""

		headers = {
			"x-api-key": "DjpcK97IzdUPQGvv9rX8FEcINrbqzZRt",
			"user-agent": "FLEU/CFNetwork/Darwin",
		}

		params = {"procedure": "2", "sku": self.releases["pid"], "address": addy}

		try:
			response = requests.get(
				"https://www.footlocker.eu/api/launch-stores",
				headers=headers,
				params=params,
				proxies=self.proxy,
			)

			if response.status_code == 403 or "url" in response.json():
				self.proxyManager.banProxy(self.proxy["https"])
				self.proxy = self.proxyManager.getProxy()
				Logger.error("Proxy banned. Switching proxy!")
				return self.promptReleases()

		except Exception as error:
			Logger.error(f"An error has occured {error} please retry.")
			return self.selectShops()

		print(response.text)
		stores = response.json()["stores"]

		if len(stores) == 0:
			Logger.error(f"No shops found 160km around {addy}!")
			return self.selectShops()

		availableShops = list()

		for store in stores:
			payload = {"id": store["id"], "name": store["displayName"]}
			availableShops.append(payload)

		"""
			Build selectShops choices like "{INDEX}. {NAME OF SHOP}
		"""

		toSelectShops = list()

		for i, shop in enumerate(availableShops):
			toSelectShops.append("{}. {}".format(i, shop["name"]))

		questions = [
			inquirer.Checkbox(
				"choice",
				message="What shop do you want to run? (Select only 3 shops!)",
				choices=toSelectShops,
			),
		]

		answers = inquirer.prompt(questions).get("choice")

		while len(answers) > 3:

			Logger.error(
				f"Please select only 3 shops max! You have select {len(answers)} shops!"
			)

			questions = [
				inquirer.Checkbox(
					"choice",
					message="What shop do you want to run? (Select only 3 shops!)",
					choices=toSelectShops,
				),
			]

			answers = inquirer.prompt(questions).get("choice")

		selectedShops = list()

		for answer in answers:
			index = answer.split(".")[0]
			selectedShops.append(availableShops[int(index)])

		return selectedShops

	def selectSizes(self, sizes):
		questions = [
			inquirer.Text(
				"size",
				message="What size do you want to enter? (min 0, max 100, separate by swoosh, in EU size)",
				default="0, 100",
			)
		]

		answer = inquirer.prompt(questions).get("size").strip()
		sizeAnswer = answer.split(",")

		if len(sizeAnswer) != 2:
			Logger.error("Error, please use: LOWEST SIZE IN NUMBER, MAX SIZE IN NUMBER")
			return self.selectSizes(sizes)

		min = float(sizeAnswer[0])
		max = float(sizeAnswer[1])

		selectedSizes = [
			x for x in sizes if float(x["eu"]) >= min and float(x["eu"]) <= max
		]

		if len(sizes) == 0:
			Logger.error("No sizes are corresponding with your demand!")
			return self.selectSizes(sizes)

		return selectedSizes
