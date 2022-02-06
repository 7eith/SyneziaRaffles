'''

[Solebox] enter_raffle.py

Author: seith <seith.corp@gmail.com>

Created: 23/04/2021 22:50:33 by seith
Updated: 23/04/2021 22:50:33 by seith

Synezia Corp. (c) 2021 - MIT

'''

import time
import random
import requests
import datetime
import json

from logger.logger import Logger
from proxy.controller import ProxyManager

class SoleboxEnterRaffle():

	def __init__(self, index, profile, raffle, userAgent):
		Logger.info(f"[{index}] Starting Task for {profile['email']}")
		self.index = index
		self.profile = profile
		self.raffle = raffle
		self.userAgent = userAgent

		""" Variables """
		self.proxy = ProxyManager().getProxy()
		self.success = False
		self.status = "FAILED"

		enterRaffleStatus: int = self.enterRaffle()

		if (enterRaffleStatus == 1):
			Logger.success(f"[{self.index}] Successfully entered {self.profile['email']}")
			self.success = True
			self.status = "SUCCESS"
			return 
		elif (enterRaffleStatus == -1):
			Logger.error(f"[{self.index}] Already registered into Raffle...")
			self.success = False
			self.status = "SUBSCRIBED"	
			return
		else:
			Logger.error(f"[{self.index}] Already registered into Raffle...")
			self.success = False
			self.status = "FAILED"

	def generateRandomTimeline(self):
		timestamp = round(time.time() * 1000)

		expando = "jQuery1.9.00."
		expando += str(random.randint(0, 9999999999999999))
		expando += "_"
		expando += str(timestamp)

		return {
			"expando": f"{expando.replace('.', '')}{str(timestamp)}",
			"submitTime": f"{str(timestamp + random.randint(1, 2))}"
		}

	def enterRaffle(self):
		timeLine = self.generateRandomTimeline()

		headers = {
    		'authority': 'solebox.us16.list-manage.com',
			'user-agent': self.userAgent,
			'accept': '*/*',
			'sec-fetch-site': 'cross-site',
			'sec-fetch-mode': 'no-cors',
			'sec-fetch-dest': 'script',
			'referer': 'https://blog.solebox.com/',
			'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7',
			'dnt': '1',
		}
		
		params = (
			('u', self.raffle['u']),
			('id', self.raffle['id']),
			('c', timeLine['expando']),
			('EMAIL', self.profile['email']),
			('FNAME', self.profile['first_name']),
			('LNAME', self.profile['last_name']),
			('PHONE', self.profile['phone']),
			# ('MMERGE6', self.profile['country']),
			(f'{self.raffle["params"]["Birthday"]}[day]', self.profile['day']),
			(f'{self.raffle["params"]["Birthday"]}[month]', self.profile['month']),
			# ('MMERGE9', self.profile['gender']),
			(f'{self.raffle["params"]["Instagram"]}', self.profile['instagram']),
			(f'{self.raffle["params"]["Store"]["fieldName"]}', self.profile['shop']),
			(f'{self.raffle["params"]["Sizes"]["fieldName"]}', self.profile['size']),
			(f"b_{self.raffle['u']}_{self.raffle['id']}", ''),
			('subscribe', 'Subscribe'),
			('_', timeLine['submitTime']), 
		)

		try:
			response = requests.get('https://solebox.us16.list-manage.com/subscribe/post-json', headers=headers, params=params, proxies=self.proxy)
		except (requests.exceptions.ProxyError, requests.exceptions.ConnectionError):
			Logger.error(f"[{self.index}] Proxy Error... Rotating...")
			ProxyManager().banProxy(self.proxy["https"])
			self.proxy = ProxyManager().getProxy()
			return self.enterRaffle()
			
		except Exception as error:
			Logger.error(f"[{self.index}] Uncatched error... {error}")
			return 

		if ("already subscribed" in response.text):
			return (-1)

		if ("success" in response.text):
			return (1)

		return (0)