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
		self.raffleURL = "https://www.streetmachine.com/draw/dunk-low-pro-acg"

		""" TwoCaptcha """
		self.solver = TwoCaptcha(Configuration().two_captcha)

		""" Task """
		logStatus: int = self.loginIntoAccount()

		if (logStatus == 1):
			self.state = "LOGGED"
			Logger.success(f"[{self.index}] Successfully login")
			self.success = False

			if (self.enterRaffle()):
				self.success = True
				self.state = "SUCCESS"
			else:
				self.state = "FAILED"

		else:			
			self.state = "FAILED"
			self.success = False
			Logger.error(f"[{self.index}] Failed to login to {self.profile['email']}")

	def loginIntoAccount(self):
		self.__initSession()

		headers = {
			'Connection': 'keep-alive',
			'Cache-Control': 'max-age=0',
			'Upgrade-Insecure-Requests': '1',
			'Origin': 'https://www.streetmachine.com',
			'Content-Type': 'application/x-www-form-urlencoded',
			'User-Agent': self.userAgent,
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'Sec-Fetch-Site': 'same-origin',
			'Sec-Fetch-Mode': 'navigate',
			'Sec-Fetch-User': '?1',
			'Sec-Fetch-Dest': 'document',
			'Referer': 'https://www.streetmachine.com/login',
			'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7',
			'dnt': '1',
		}

		data = {
			'formid': 'login',
			'email': self.profile['email'],
			'password': self.profile['password']
		}

		try:
			response = self.session.post('https://www.streetmachine.com/login', headers=headers, data=data, proxies=self.proxy, allow_redirects=False)
		except Exception as error:
			Logger.error(f"[{self.index}] {error}")
			ProxyManager().banProxy(self.proxy)
			return (-1)

		if (response.status_code == 302):
			return (1)
		else:
			return (-1)

	def enterRaffle(self):

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
			Logger.error(f"[{self.index}] Failed to entry into Raffle...")
			return False

		if ("You are now participating in this draw." in response.text or "Du deltager" in response.text):
			Logger.success(f"[{self.index}] Successfully entred into raffle {self.profile['email']}")
			return True
		else:
			Logger.error(f"[{self.index}] Failed to entry {self.profile['email']}")
			return False
		