'''

[account] create_account.py

Author: seith <seith.corp@gmail.com>

Created: 03/04/2021 18:09:03 by seith
Updated: 03/04/2021 18:09:03 by seith

Synezia Corp. (c) 2021 - MIT

'''

import requests
import random
import re

from proxy.controller import ProxyManager
from logger.logger import Logger
from configuration.configuration import Configuration

class EnterRaffle():

	def __init__(self, index, profile):
		Logger.info(f"[{index}] Starting Task for {profile['email']}...")

		""" Values """
		self.index = index
		self.profile = profile

		self.success = False
		self.proxy = ProxyManager().getProxy()

		if (self.enterRaffle()):
			self.state = "SUCCESS"
			self.success = True
			Logger.success(f"[{self.index}] Successfully entered into Raffle [{self.profile['email']}]")
		else:			
			self.state = "FAILED"
			self.success = False
			Logger.error(f"[{self.index}] Failed to enter {self.profile['email']}")

	def enterRaffle(self):
		headers = {
			'authority': 'n2ogl6wnm0.execute-api.us-east-1.amazonaws.com',
			'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
			'accept': 'application/json, text/plain, */*',
			'sec-ch-ua-mobile': '?0',
			'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
			'origin': 'https://shop.travisscott.com',
			'sec-fetch-site': 'cross-site',
			'sec-fetch-mode': 'cors',
			'sec-fetch-dest': 'empty',
			'referer': 'https://shop.travisscott.com/',
			'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7',
			'dnt': '1',
		}

		params = (
			('a', 'm'),
			('email', self.profile['email']),
			('first', self.profile['firstName']),
			('last', self.profile['lastName']),
			('zip', self.profile['zipCode']),
			('telephone', self.profile['phone']),
			('product_id', '6535691141247'),
			('kind', 'shoe'),
			('size', self.profile['size']),
		)

		try:
			response = requests.get('https://n2ogl6wnm0.execute-api.us-east-1.amazonaws.com/production/adult', headers=headers, params=params, proxies=self.proxy)
		except (requests.exceptions.ProxyError, requests.exceptions.ConnectionError):
			Logger.error(f"[{self.index}] Proxy Error - Rotating...")
			ProxyManager().banProxy(self.proxy["https"])
			self.proxy = ProxyManager().getProxy()
			return self.enterRaffle()
		except Exception as error:
			Logger.error(f"[{self.index}]{error}")
			Logger.error(f"[{self.index}] Failed to entry into Raffle...")
			return False

		print(response.text)

		if (response.text):
			if ("thanks" in response.text):
				return True
			else:
				return False