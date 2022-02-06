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

from twocaptcha import TwoCaptcha

from proxy.controller import ProxyManager
from logger.logger import Logger
from configuration.configuration import Configuration

class EnterRaffle():

	def __initSession(self):
		try:
			self.ipAddress = requests.get('https://api.ipify.org/?format=json', proxies=self.proxy).json()['ip']
			self.session.cookies.set("bbc", self.ipAddress, domain="www.streetmachine.com")
		except Exception as error:
			Logger.error(f"[{self.index}]{error}")
			Logger.error(f"[{self.index}] Failed to connect to Proxy. Rotating...")
			ProxyManager().banProxy(self.proxy)
			self.__initSession()

	def __init__(self, index, profile, loggerFileName, userAgent):
		Logger.info(f"[{index}] Starting Task for {profile['email']}...")

		""" Values """
		self.index = index
		self.profile = profile
		self.loggerFileName = loggerFileName
		self.userAgent = userAgent

		self.success = False
		self.session = requests.Session()
		self.proxy = ProxyManager().getProxy()

		if (self.enterRaffle()):
			self.state = "SUCCESS"
			self.success = True
			Logger.success(f"[{self.index}] Successfully entered into Raffle [{self.profile['email']}]")
		else:			
			self.state = "FAILED"
			self.success = False
			Logger.error(f"[{self.index}] Failed to login to {self.profile['email']}")

	def enterRaffle(self):
		headers = {
			'authority': 'dem.ixorateam.com',
			'cache-control': 'max-age=0',
			'upgrade-insecure-requests': '1',
			'origin': 'https://www.theplayoffs.com',
			'content-type': 'application/x-www-form-urlencoded',
			'user-agent': self.userAgent,
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'sec-fetch-site': 'cross-site',
			'sec-fetch-mode': 'navigate',
			'sec-fetch-user': '?1',
			'sec-fetch-dest': 'document',
			'referer': 'https://www.theplayoffs.com/',
			'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7',
			'dnt': '1',
		}

		data = {
			'js_id': '6b39',
			'from_url': 'yes',
			'hdn_email_txt': '',
			'sib_simple': 'simple',
			'sib_forward_url': 'https://www.theplayoffs.com/raffle-subscribed/',
			'req_hid': '~NOME~COGNOME~ACCOUNT_INSTAGRAM~CITTA~INDIRIZZO~CAP~PAGAMENTO~TELEFONO~NAZIONE~SIZE_SHOES',
			'email': self.profile['email'],
			'NOME': self.profile['first_name'],
			'COGNOME': self.profile['last_name'],
			'ACCOUNT_INSTAGRAM': self.profile['instagram'],
			'SIZE_SHOES': self.profile['size'],
			'PAGAMENTO': self.profile['payment'],
			'NAZIONE': self.profile['country'],
			'CITTA': self.profile['city'],
			'INDIRIZZO': self.profile['address'],
			'CAP': self.profile['zipCode'],
			'TELEFONO': self.profile['phone']
		}

		try:
			response = self.session.post('https://dem.ixorateam.com/users/subscribeembed/js_id/6b39/id/1', headers=headers, data=data, proxies=self.proxy)
		except Exception as error:
			Logger.error(f"[{self.index}]{error}")
			Logger.error(f"[{self.index}] Failed to entry into Raffle...")
			return False

		if (response.url == "https://www.theplayoffs.com/raffle-subscribed/"):
			return True
		else:
			return False
		