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
from .enter import FootLockerEnterAccount

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

		self.promptSettings()

		"""
			UI
		"""

		printHeader()
		printLine()

		"""
			HELLO MULTITHREADING
		"""

		with ThreadPoolExecutor(max_workers=self.threadsNumber) as executor:
			for i, profile in enumerate(profiles):
				executor.submit(
					FootLockerEnterAccount,
					profile,
					self.sizes,
					self.shops,
					self.releases["pid"],
					i,
				)


		# for i, profile in enumerate(profiles):
		# 	FootLockerEnterAccount(profile, self.sizes, self.shops, self.releases["pid"], i)

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
				"Check your response, threads number need to be a Integer between 1-4200"
			)
			return self.promptThreadsNumber()

		if threads < 1:
			Logger.error(
				"Check your response, threads number need to be a Integer between 1-4200"
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
				"https://www.footlocker.be/apigate/session",
				headers=headers,
				proxies=self.proxy,
			)
			print(response.text)
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
			'authority': 'www.footlocker.be',
			'cache-control': 'max-age=0',
			'upgrade-insecure-requests': '1',
			'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'sec-fetch-site': 'none',
			'sec-fetch-mode': 'navigate',
			'sec-fetch-user': '?1',
			'sec-fetch-dest': 'document',
			'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7',
			'dnt': '1',
		}

		try:
			response = requests.get(
				"https://www.footlocker.fr/apigate/release-calendar",
				headers=headers
			)

			# print(response.text)
			print(self.proxy)
			# print(response.text)
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
			'authority': 'www.footlocker.be',
			'cache-control': 'max-age=0',
			'upgrade-insecure-requests': '1',
			'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'sec-fetch-site': 'none',
			'sec-fetch-mode': 'navigate',
			'sec-fetch-user': '?1',
			'sec-fetch-dest': 'document',
			'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7',
			'dnt': '1',
			"x-api-key": "DjpcK97IzdUPQGvv9rX8FEcINrbqzZRt"
		}

		print(self.releases["pid"])

		params = {"procedure": "2", "sku": self.releases["pid"], "address": addy}

		try:
			response = requests.get(
				"https://www.footlocker.fr/apigate/launch-stores",
				headers=headers,
				params=params,
			)

			print(response.text)

			if response.status_code == 403 or "url" in response.json():
				self.proxyManager.banProxy(self.proxy["https"])
				self.proxy = self.proxyManager.getProxy()
				Logger.error("Proxy banned. Switching proxy!")
				return self.promptReleases()

		except Exception as error:
			Logger.error(f"An error has occured {error} please retry.")
			return self.selectShops()

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

		while len(answers) > 3 or len(answers) == 0:

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
