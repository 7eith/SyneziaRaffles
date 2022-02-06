import time
import random
import requests
import datetime
import json
from configuration import Configuration

from twocap import TwoCaptcha

from logger.logger import Logger
from proxy.controller import ProxyManager

class EnterRaffle():

	def __init__(self, index, profile, raffle, userAgent):
		self.index = index
		self.profile = profile
		self.raffle = raffle
		self.userAgent = userAgent

		self.proxy = ProxyManager().getProxy()
		self.success = False
		self.status = "FAILED"

		self.solver = TwoCaptcha(Configuration().two_captcha, pollingInterval=3, softId=2815)
		Logger.info(f"[{self.index}] Solving Captcha...")

		try:
			self.captchaToken = self.solver.recaptcha(sitekey='6LfbPnAUAAAAACqfb_YCtJi7RY0WkK-1T4b9cUO8', url=self.raffle['url'])['code']
		except Exception as error:
			Logger.error(f"Failed to solve Captcha! Error: {error}")
			return 
		Logger.info(f"[{self.index}] Captcha Solved!")

		enterRaffleStatus: int = self.enterRaffle()

		if (enterRaffleStatus == 1):
			Logger.success(f"[{self.index}] Successfully entered {self.profile['email']}")
			self.success = True
			self.status = "SUCCESS"
		elif (enterRaffleStatus == -1):
			Logger.error(f"[{self.index}] Already registered into Raffle...")
			self.success = False
			self.status = "SUBSCRIBED"	
		else:
			Logger.error(f"[{self.index}] Failed to register into Raffle...")
			self.success = False
			self.status = "FAILED"

	def enterRaffle(self):

		headers = {
			'authority': 'www.nakedcph.com',
			'cache-control': 'max-age=0',
			'upgrade-insecure-requests': '1',
			'origin': 'https://www.nakedcph.com',
			'content-type': 'application/x-www-form-urlencoded',
			'user-agent': self.userAgent,
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'sec-fetch-site': 'cross-site',
			'sec-fetch-mode': 'navigate',
			'sec-fetch-user': '?1',
			'sec-fetch-dest': 'document',
			'referer': 'https://www.nakedcph.com/',
			'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7',
			'dnt': '1',
			'Referer': 'https://www.nakedcph.com/',
			'Origin': 'https://www.nakedcph.com',
			'User-Agent': self.userAgent,
		}

		data = {
			'tags[]': self.raffle['raffle_tag'],
			'token': 'c812c1ff-2a5a0fe-efad139-d754416-71e1e60-2ce',
			'rule_email': self.profile['email'],
			'fields[Raffle.Instagram Handle]': self.profile['instagram'],
			'fields[Raffle.Phone Number]': self.profile['phone'],
			'fields[Raffle.First Name]': self.profile['first_name'],
			'fields[Raffle.Last Name]': self.profile['last_name'],
			'fields[Raffle.Shipping Address]': self.profile['address'],
			'fields[Raffle.Postal Code]': self.profile['zipCode'],
			'fields[Raffle.City]': self.profile['city'],
			'fields[Raffle.Country]': self.profile['countryCode'],
			'fields[SignupSource.ip]': '192.0.0.1',
			'fields[SignupSource.useragent]': 'Mozilla',
			'language': 'sv',
			'g-recaptcha-response': self.captchaToken
		}

		try:
			response = requests.post('https://app.rule.io/subscriber-form/subscriber', headers=headers, data=data, allow_redirects=False, proxies=self.proxy)
		except (requests.exceptions.ProxyError, requests.exceptions.ConnectionError):
			Logger.error(f"[{self.index}] Proxy Error... Rotating...")
			ProxyManager().banProxy(self.proxy["https"])
			self.proxy = ProxyManager().getProxy()
			return self.enterRaffle()
			
		except Exception as error:
			Logger.error(f"[{self.index}] Uncatched error... {error}")
			return 

		if (response.status_code == 302):
			redirectURI = response.headers['Location']

			if ("successful" in redirectURI):
				return (1)

		return (0)