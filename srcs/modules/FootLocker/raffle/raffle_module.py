'''

[raffle] raffle_module.py

Author: seith <seith.corp@gmail.com>

Created: 12/04/2021 12:36:04 by seith
Updated: 12/04/2021 12:36:04 by seith

Synezia Corp. (c) 2021 - MIT

'''

import PyInquirer
import requests

from singleton.controller import Instance
from profiles import Profile
from proxy.controller import ProxyManager

from configuration.configuration import Configuration
from utils.colors import Color
from logger.logger import Logger

from .enter_raffle import FootLockerEnterRaffle
from concurrent.futures import ThreadPoolExecutor, as_completed


class RaffleModule():

	def monitor(self):
		pass

	def __init__(self):
		Instance().updateRPC("Setup FootLocker Raffle...")

		""" Variables """
		version = "0.0.1-BETA"
		moduleName = "FootLocker"
		action = "Enter_Raffle"
		date = Instance().getDate()
		loggerFileName = f"logs/{moduleName}/{action}.csv"

		""" Proxy """ 
		self.proxyManager = ProxyManager(moduleName)
		self.proxy = self.proxyManager.getProxy()

		""" Profiles """
		profile = Profile(moduleName)
		self.profiles = profile.fetchProfiles()


		self.__promptSettings()

		for i, profile in enumerate(self.profiles):
			FootLockerEnterRaffle(i, profile, None, None, None)

		# FootLockerEnterRaffle(0, self.profiles[0], self.sizes, self.shops, self.release['pid'])

	def __promptSettings(self):
		self.release = self.promptReleases()
		self.shops = self.promptShops()
		self.sizes = self.selectSizes(self.release['sizes'])

	""" Settings """

	def promptReleases(self):

		headers = {
			'user-agent': 'FLEU/CFNetwork/Darwin',
		}

		try:
			response = requests.get('https://www.footlocker.fr/apigate/release-calendar', headers=headers, proxies=self.proxy)
		except Exception as error:
			Logger.error(error)
			ProxyManager().banProxy(self.proxy["https"])
			self.proxy = ProxyManager().getProxy()
			return self.promptReleases()

		""" Filter Releases """
		releases = response.json()["releaseCalendarProducts"]
		releaseReservation = [x for x in releases if "reservation" in x]

		activeReleases = [
			x for x in releaseReservation if x["reservation"]["statusCode"] > 0
		]

		""" Setup Prompt """
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
			{
				'type': 'list',
				'name': 'choice',
				'message': 'Select Raffle',
				'choices': releasesNames	
			}
		]

		answer = (
			PyInquirer.prompt(questions=questions, keyboard_interrupt_msg=f"{Color.RED}Cancelled by User. Exiting CLI{Color.RESET}")
			.get("choice")
		)

		if not answer:
			exit(0)

		selectedRaffle = [x for x in formatedReleases if str(answer) in x["name"]]
		return selectedRaffle[0]

	def promptShops(self):
		""" Handle City/Addy """
		questions = [
			{
				'type': 'input',
				'name': 'addy',
				'message': 'Enter a city or an address',
			},
		]

		addy = (
			PyInquirer.prompt(questions=questions, keyboard_interrupt_msg=f"Cancelled by User. Exiting CLI")
			.get("addy")
		)

		""" Requests Shops """
		headers = {
			'user-agent': 'FLEU/CFNetwork/Darwin',
		}

		params = {
			"procedure": "2", 
			"sku": self.release["pid"],
			"address": addy
		}

		response = requests.get('https://www.footlocker.fr/apigate/launch-stores', headers=headers, params=params, proxies=self.proxy)
		stores = response.json()["stores"]

		""" Prompt Shops """
		availableShops = list()

		for store in stores:
			payload = {"id": store["id"], "name": store["displayName"]}
			availableShops.append(payload)

		"""
			Build selectShops 
		"""

		toSelectShops = list()

		for i, shop in enumerate(availableShops):
			payload = {
				'name': shop['name'],
				'value': shop['id']
			}
			toSelectShops.append(payload)

		questions = [
			{
				'type': 'checkbox',
				'name': 'selectedShops',
				'message': 'Select Shop(s) Max: 3',
				'choices': toSelectShops	
			}
		]

		answer = (
			PyInquirer.prompt(questions=questions, keyboard_interrupt_msg=f"{Color.RED}Cancelled by User. Exiting CLI{Color.RESET}")
			.get("selectedShops")
		)

		while len(answer) > 3 or len(answer) == 0:

			Logger.error(
				f"Please select only 3 shops max! You have selected {len(answer)} shops!"
			)

			questions = [
				{
					'type': 'checkbox',
					'name': 'selectedShops',
					'message': 'Select Shop(s) Max: 3',
					'choices': toSelectShops	
				}
			]

			answer = (
				PyInquirer.prompt(questions=questions, keyboard_interrupt_msg=f"{Color.RED}Cancelled by User. Exiting CLI{Color.RESET}")
			)

		return answer

	def selectSizes(self, sizes):
		questions = [
			{
				'type': 'input',
				'name': 'size',
				'message': 'What size do you want to enter? (min 0, max 100, separate by swoosh, in EU size)',
				'default': '0, 100'
			},
		]

		answer = (
			PyInquirer.prompt(questions=questions, keyboard_interrupt_msg=f"Cancelled by User. Exiting CLI")
			.get("size")
		)

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
