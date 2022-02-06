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
import string
import datetime
import json

from configuration import Configuration

from twocap import TwoCaptcha

from logger.logger import Logger
from proxy.controller import ProxyManager
from requests_toolbelt import MultipartEncoder


class ImpactEnterRaffle():

	def __init__(self, index, profile, raffle, userAgent):
		Logger.info(f"[{index}] Starting Task for {profile['email']}")
		self.index = index
		self.profile = profile
		self.raffle = raffle
		self.userAgent = userAgent

		""" Variables """
		self.solver = TwoCaptcha(Configuration().two_captcha, pollingInterval=3, softId=2815)
		self.proxy = ProxyManager().getProxy()
		self.session = requests.Session()
		self.success = False
		self.status = "FAILED"

		Logger.info(f"[{self.index}] Solving Captcha...")

		try:
			self.captchaToken = self.solver.recaptcha(sitekey='6LdgCYoaAAAAAOiwh9Vi_rpwp3I31r4WrE7IfMKa', url="https://www.impact-premium.com/cf/raffle-1")['code']
		except Exception as error:
			Logger.error(f"Failed to solve Captcha! Error: {error}")
			return 
		Logger.info(f"[{self.index}] Captcha Solved!")
		
		enterRaffleStatus = self.enterRaffle()

		if (enterRaffleStatus):
			Logger.success(f"[{self.index}] Successfully entered {self.profile['email']}")
			self.success = True
			self.status = "SUCCESS"
			return 
		else:
			Logger.error(f"[{self.index}] Error has occured when registering {self.profile['email']}...")
			self.success = False
			self.status = "FAILED"

	def initSession(self):
		headers = {
			'authority': 'www.impact-premium.com',
			'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
			'sec-ch-ua-mobile': '?0',
			'upgrade-insecure-requests': '1',
			'user-agent': self.userAgent,
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'sec-fetch-site': 'none',
			'sec-fetch-mode': 'navigate',
			'sec-fetch-user': '?1',
			'sec-fetch-dest': 'document',
			'accept-language': 'en-US,en;q=0.9',
		}

		try:
			response = self.session.get('https://www.impact-premium.com/cf/concours-3', headers=headers, proxies=self.proxy)
		except (requests.exceptions.ProxyError, requests.exceptions.ConnectionError):
			Logger.error(f"[{self.index}] Proxy Error... Rotating...")
			ProxyManager().banProxy(self.proxy["https"])
			self.proxy = ProxyManager().getProxy()
			return self.initSession()
			
		except Exception as error:
			Logger.error(f"[{self.index}] Uncatched error... {error}")
			return (False)
		return (True)

	def enterRaffle(self):

		if (self.initSession()):
			shippingType = "Envoi Postal"
			paymentType = "Paypal"

			if ("shipping" in self.profile and self.profile['shipping'] == "Pickup-Strasbourg"):
				shippingType = "Retrait en magasin (Strasbourg)"
			elif ("shipping" in self.profile and self.profile['shipping'] == "Pickup-Mulhouse"):
				shippingType = "Retrait en magasin (Mulhouse)"
			
			if ("payment" in self.profile and self.profile['payment'] == "Instore"):
				paymentType = "En Boutique"

			fields = {
				"c_pointure": self.profile['size'],
				"c_name": self.profile['lastname'],
				"c_prenom": self.profile['firstname'],
				"c_adresse": self.profile['addy'],
				"c_code_postal": self.profile['zip'],
				"c_ville": self.profile['city'],
				"c_myemail": self.profile['email'],
				"c_numero_telephone": self.profile['phone'],
				"c_pays": self.profile['country'],
				"c_paiement": paymentType,
				"c_livraison": shippingType,
				"g-recaptcha-response": self.captchaToken,
				"submitform": "Valider mon inscription",
				"fid": '1'
			}

			boundary = '----WebKitFormBoundary' + ''.join(random.sample(string.ascii_letters + string.digits, 16))
			m = MultipartEncoder(fields=fields, boundary=boundary)

			# headers = {
			# 	'authority': 'www.impact-premium.com',
			# 	'cache-control': 'max-age=0',
			# 	'upgrade-insecure-requests': '1',
			# 	'origin': 'https://www.impact-premium.com',
			# 	'content-type': m.content_type,
			# 	'user-agent': self.userAgent,
			# 	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			# 	'sec-fetch-site': 'same-origin',
			# 	'sec-fetch-mode': 'navigate',
			# 	'sec-fetch-user': '?1',
			# 	'sec-fetch-dest': 'document',
			# 	'referer': 'https://www.impact-premium.com/cf/raffle-1',
			# 	'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7',
			# 	'dnt': '1',
			# }

			
			headers = {
				'authority': 'www.impact-premium.com',
				'cache-control': 'max-age=0',
				'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
				'sec-ch-ua-mobile': '?0',
				'upgrade-insecure-requests': '1',
				'origin': 'https://www.impact-premium.com',
				'content-type': m.content_type,
				'user-agent': self.userAgent,
				'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
				'sec-fetch-site': 'same-origin',
				'sec-fetch-mode': 'navigate',
				'sec-fetch-user': '?1',
				'sec-fetch-dest': 'document',
				'referer': 'https://www.impact-premium.com/cf/raffle-1',
				'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7',
				'dnt': '1',
			}

			try:
				response = self.session.post('https://www.impact-premium.com/cf', headers=headers, data=m, proxies=self.proxy)
			except (requests.exceptions.ProxyError, requests.exceptions.ConnectionError):
				Logger.error(f"[{self.index}] Proxy Error... Rotating...")
				ProxyManager().banProxy(self.proxy["https"])
				self.proxy = ProxyManager().getProxy()
				return self.enterRaffle()
				
			except Exception as error:
				Logger.error(f"[{self.index}] Uncatched error... {error}")
				return (False)

			if ("raffle-confirmation" in response.url):
				return (True)

			return (False)