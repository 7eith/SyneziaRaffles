'''

[aio] aio_task.py

Author: seith <seith.corp@gmail.com>

Created: 03/04/2021 18:48:51 by seith
Updated: 03/04/2021 18:48:51 by seith

Synezia Corp. (c) 2021 - MIT

'''

import requests
import random

from proxy.controller import ProxyManager
from logger.logger import Logger
from configuration.configuration import Configuration
from twocaptcha import TwoCaptcha

class AIOTask():


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

		self.raffleURL = "https://www.streetmachine.com/draw/dunk-low-pro-acg"

		""" Values """
		self.index = index
		self.profile = profile
		self.loggerFileName = loggerFileName
		self.userAgent = userAgent

		self.success = False
		self.session = requests.Session()
		self.proxy = ProxyManager().getProxy()

		""" TwoCaptcha """
		self.solver = TwoCaptcha(Configuration().two_captcha)

		if (self.createAccount()):
			self.state = "CREATED"
			Logger.success(f"[{self.index}] Successfully registered {self.profile['email']} on StreetMachine!")

			if (self.enterRaffle()):
				self.success = True
				self.state = "ALL"
			else:
				self.state = "FAILED"
			
		else:
			self.state = "REGISTERED"
			Logger.error(f"[{self.index}] Already registered {self.profile['email']}...")

	def createAccount(self):
		self.__initSession()

		headers = {
			'Host': 'www.streetmachine.com',
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': self.userAgent,
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'Sec-Fetch-Site': 'same-origin',
			'Sec-Fetch-Mode': 'navigate',
			'Sec-Fetch-Dest': 'document',
			'Referer': 'https://www.streetmachine.com/bbc?urlbbc=/register',
			'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7',
			'dnt': '1',
			'Pragma': 'no-cache',
			'Cache-Control': 'no-cache',
		}

		try:
			response = self.session.get('https://www.streetmachine.com/register', proxies=self.proxy, headers=headers)
		except Exception as error:
			Logger.error(f"[{self.index}]{error}")
			Logger.error(f"[{self.index}] Proxy Error. Rotating...")
			ProxyManager().banProxy(self.proxy)
			self.session = requests.Session()
			self.proxy = ProxyManager().getProxy()
			return self.createAccount()

		Logger.info(f"[{self.index}] Session Initialized...")

		""" Captcha """
		Logger.info(f"[{self.index}] Requesting Captcha...")
		solvedCaptchaToken = self.solver.solve_captcha(site_key='6LdrwtsUAAAAAGDa_VbZYCmmiFowrFZb_562hphY', page_url='https://www.streetmachine.com/register')
		Logger.info(f"[{self.index}] Successfully fetched Captcha!")

		headers = {
			'User-Agent': self.userAgent,
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
			'Referer': 'https://www.streetmachine.com/register',
			'Content-Type': 'application/x-www-form-urlencoded',
			'Origin': 'https://www.streetmachine.com',
			'Connection': 'keep-alive',
			'Upgrade-Insecure-Requests': '1',
			'Cache-Control': 'max-age=0',
		}

		data = {
			'formid': 'register',
			'g-recaptcha-response': solvedCaptchaToken,
			'first_name': self.profile['first_name'],
			'surname': self.profile['last_name'],
			'email': self.profile['email'],
			'password': self.profile['password'],
			'password_repeat': self.profile['password']
		}

		try:
			response = self.session.post('https://www.streetmachine.com/account', headers=headers, data=data, proxies=self.proxy)
		except Exception as error:
			Logger.error(f"[{self.index}]{error}")
			Logger.error(f"[{self.index}] Proxy Error. Rotating...")
			ProxyManager().banProxy(self.proxy)
			self.session = requests.Session()
			self.proxy = ProxyManager().getProxy()
			return self.createAccount()

		if ("form-error" in response.text):
			return False
		else:
			return True

	def enterRaffle(self):
		Logger.info(f"[{self.index}] Starting to entering into Raffle for {self.profile['email']}...")

		""" Captcha """
		Logger.info(f"[{self.index}] Requesting Captcha...")
		solvedCaptchaToken = self.solver.solve_captcha(site_key='6LdrwtsUAAAAAGDa_VbZYCmmiFowrFZb_562hphY', page_url=self.raffleURL)
		Logger.info(f"[{self.index}] Successfully fetched Captcha!")

		headers = {
			'Host': 'www.streetmachine.com',
			'Cache-Control': 'no-cache',
			'Upgrade-Insecure-Requests': '1',
			'Origin': 'https://www.streetmachine.com',
			'User-Agent': self.userAgent,
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'Sec-Fetch-Site': 'same-origin',
			'Sec-Fetch-Mode': 'navigate',
			'Sec-Fetch-User': '?1',
			'Sec-Fetch-Dest': 'document',
			'Referer': self.raffleURL,
			'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7',
			'dnt': '1',
			'Pragma': 'no-cache',
		}

		data = {
			'formid': 'draw',
			'g-recaptcha-response': solvedCaptchaToken,
			'item_pid': str(random.randint(338189,338197))
			# 'option:42': 'on'
		}

		try:
			response = self.session.post(self.raffleURL, headers=headers, data=data, proxies=self.proxy)
		except Exception as error:
			Logger.error(f"[{self.index}]{error}")
			Logger.error(f"[{self.index}] Cancelling entry. (Safe Mode)")
			return False

		if ("You are now participating in this draw." in response.text or "Du deltager" in response.text):
			Logger.success(f"[{self.index}] Successfully Created & Entred {self.profile['email']}")
			return True
		else:
			Logger.error(f"[{self.index}] Failed to entry {self.profile['email']} but he registered into StreetMachine")
			return False