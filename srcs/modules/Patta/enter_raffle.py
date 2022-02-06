'''

[Patta] account_create.py

Author: seith <seith.corp@gmail.com>

Created: 26/02/2021 13:10:47 by seith
Updated: 26/02/2021 13:10:47 by seith

Synezia Corp. (c) 2021 - MIT

'''

import requests
import re
import json

from utils.cli_utils import printHeader, printLine
from utils.colors import Color

from logger.logger import Logger
from proxy.controller import ProxyManager
from controller.profile_parser import fetchProfiles
from concurrent.futures import ThreadPoolExecutor, as_completed

from random_user_agent.user_agent import UserAgent
user_agent_rotator = UserAgent(software_names=['chrome', 'edge', 'opera', 'firefox', 'android-browser'], operating_systems=['windows', 'linux', 'macos', 'android', 'ios'])

class PattaRaffle():

	def __init__(self):
		self.proxyManager = ProxyManager()
		self.profiles = fetchProfiles("Patta")

		processes = []
		with ThreadPoolExecutor(max_workers=15) as executor:
			 for i, profile in enumerate(self.profiles):
				 processes.append(executor.submit(self.enterRaffle, profile))

	def enterRaffle(self, profile):
		Logger.info('[Patta] Logging-in')

		proxy = self.proxyManager.getProxy()
		userAgent = user_agent_rotator.get_random_user_agent()
		session = requests.Session()

		headers = {
			'Host': 'www.patta.nl',
			'cache-control': 'no-cache',
			'upgrade-insecure-requests': '1',
			'origin': 'https://www.patta.nl',
			'content-type': 'application/x-www-form-urlencoded',
			'user-agent': userAgent,
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'sec-fetch-site': 'same-origin',
			'sec-fetch-mode': 'navigate',
			'sec-fetch-user': '?1',
			'sec-fetch-dest': 'document',
			'referer': 'https://www.patta.nl/account/login',
			'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7',
			'dnt': '1',
			'pragma': 'no-cache',
		}

		data = 'form_type=customer_login&utf8=%E2%9C%93' 
		data += '&customer%5Bemail%5D=' 
		data += profile['email']
		data += '&customer%5Bpassword%5D=' 
		data += profile['password']

		response = requests.post('https://www.patta.nl/account/login', headers=headers, data=data, proxies=proxy)

		if ("CustomerEmail" in response.text):
			Logger.info('[Patta] Logged-in')

		customerIdMatcher = re.search('"CustomerId": "(.+?)",', response.text)
		customerId = customerIdMatcher.group(1)

		headers = {
			'Host': 'patta-raffle.vercel.app',
			'user-agent': userAgent,
			'content-type': 'text/plain;charset=UTF-8',
			'accept': '*/*',
			'origin': 'https://www.patta.nl',
			'sec-fetch-site': 'cross-site',
			'sec-fetch-mode': 'cors',
			'sec-fetch-dest': 'empty',
			'referer': 'https://www.patta.nl/',
			'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7',
			'dnt': '1',
			'pragma': 'no-cache',
			'cache-control': 'no-cache',
		}

		accountProfile = {
			"firstName": profile['name'],
			"lastName": profile['surname'],
			"customerId": customerId,
			"email": profile['email'],
			"productID": "4874845061155",
			"productSizeSKU": "DB0732-200-US10.5",
			"productVariantId": "33039719727139",
			"productSlug": "air-jordan-4-retro-taupe-haze-infrared-23-oil-grey",
			"raffleId": "555412389923",
			"raffleName": "air-jordan-4-retro-taupe-haze-infrared-23-oil-grey",
			"streetAddress": profile['address'],
			"zipCode": profile['zipCode'],
			"city": profile['city'],
			"country": profile['country'],
			"bday": profile['birthday'],
			"instagram": profile['instagram'],
			"newsletter": "false",
		}

		userRegister = json.dumps(accountProfile, separators=(",", ":"))

		response = requests.post('https://patta-raffle.vercel.app/api/postRaffleEntry/', headers=headers, data=userRegister, proxies=proxy)
		print(response.text)
		print(response.status_code)

		if (response.json()['message'] == "Added to raffle form"):
			Logger.success('Successfully entry')
		else:
			Logger.error('Failed to entered into Raffle')