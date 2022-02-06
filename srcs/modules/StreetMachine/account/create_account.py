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

class CreateAccount():

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
		Logger.info(f"[{index}] Creating {profile['email']}...")

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

		""" Task """
		accountStatus: int = self.createAccount()

		if (accountStatus == 1):
			self.state = "CREATED"
			Logger.success(f"[{self.index}] Successfully registered {self.profile['email']} on StreetMachine!")
			self.success = True
			self.state = "CREATED"
		else:
			if (accountStatus == 2): # 2 = REGISTERED
				self.state = "REGISTERED"
				self.success = True
				Logger.error(f"[{self.index}] {self.profile['email']} is already registered...")
				return
			
			self.state = "FAILED"
			self.success = False
			Logger.error(f"[{self.index}] Failed to register {self.profile['email']}")

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
		try:
			solvedCaptchaToken = self.solver.solve_captcha(site_key='6LdrwtsUAAAAAGDa_VbZYCmmiFowrFZb_562hphY', page_url='https://www.streetmachine.com/register')
		except IndexError:
			Logger.error(f"[{self.index}] Failed to handle 2Captcha...")
			return self.createAccount()
			
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
			errorMessageMatcher = re.search('<span class="form-error">(.+?)</span>', response.text)
			errorMessage = errorMessageMatcher.group(1)

			if ("registered" in errorMessage):
				return (2)
			
			Logger.error(f"[{self.index}] Error has occured: '{errorMessage}'")
			return (0)
		else:
			return (1)