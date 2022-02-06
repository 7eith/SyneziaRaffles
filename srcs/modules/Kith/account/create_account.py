import time
import random
import requests
import datetime
import json

from logger.logger import Logger
from proxy.controller import ProxyManager

class CreateAccount():

	def __init__(self, index, profile,userAgent):
		self.index = index
		self.profile = profile
		self.userAgent = userAgent

		self.proxy = ProxyManager().getProxy()
		self.success = False
		self.status = "FAILED"
		self.session = requests.Session()

		accountStatus: int = self.createAccount()

		if (accountStatus == 1):
			Logger.success(f"[{self.index}] Successfully created {self.profile['email']}")
			self.success = True
			self.status = "CREATED"

			if (self.setAddy()):
				self.success = True
				self.status = "SUCCESS"
				Logger.success(f"[{self.index}] {self.profile['email']} is now ready!")

			else:
				self.success = True
				self.status = "CREATED"
		elif (accountStatus == 2):
			Logger.error(f"[{self.index}] Email already registered ({self.profile['email']})")
			self.success = False
			self.status = "REGISTERED"
		else:
			Logger.error(f"[{self.index}] Error has occured")
			self.success = False
			self.status = "FAILED"

	def createAccount(self):
		Logger.info(f"[{self.index}] Creating account...")
		headers = {
			'Host': 'eu.kith.com',
			'cache-control': 'no-cache',
			'upgrade-insecure-requests': '1',
			'origin': 'https://eu.kith.com',
			'content-type': 'application/x-www-form-urlencoded',
			'user-agent': self.userAgent,
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'sec-fetch-site': 'same-origin',
			'sec-fetch-mode': 'navigate',
			'sec-fetch-user': '?1',
			'sec-fetch-dest': 'document',
			'referer': 'https://eu.kith.com/account/register',
			'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7',
			'dnt': '1',
			'pragma': 'no-cache',
		}

		data = {
			"form_type": "create_customer",
			"utf8": "✓",
			"customer[first_name]": self.profile['first_name'],
			"customer[last_name]": self.profile['last_name'],
			"customer[email]": self.profile['email'],
			"customer[password]":  self.profile['password']
		}

		try:
			response = self.session.post('https://eu.kith.com/account', headers=headers, data=data, allow_redirects=False, proxies=self.proxy)
		except (requests.exceptions.ProxyError, requests.exceptions.ConnectionError):
			Logger.error(f"[{self.index}] Proxy Error... Rotating...")
			ProxyManager().banProxy(self.proxy["https"])
			self.proxy = ProxyManager().getProxy()
			return self.createAccount()
			
		except Exception as error:
			Logger.error(f"[{self.index}] Uncatched error... {error}")
			return 

		if (response.status_code == 302):
			redirectURI = response.headers['Location']

			if ("challenge" in redirectURI):
				Logger.error(f"[{self.index}] Rotating Proxy...")
				ProxyManager().banProxy(self.proxy["https"])
				self.proxy = ProxyManager().getProxy()
				return self.createAccount()

			if (redirectURI == "https://eu.kith.com/account/register"):
				return (2)
			if (redirectURI == "https://eu.kith.com/"):
				return (1)
		return (0)

	def setAddy(self):
		Logger.info(f"[{self.index}] Setup Addresse...")
		headers = {
			'Host': 'eu.kith.com',
			'cache-control': 'no-cache',
			'upgrade-insecure-requests': '1',
			'origin': 'https://eu.kith.com',
			'content-type': 'application/x-www-form-urlencoded',
			'user-agent': self.userAgent,
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'sec-fetch-site': 'same-origin',
			'sec-fetch-mode': 'navigate',
			'sec-fetch-user': '?1',
			'sec-fetch-dest': 'document',
			'referer': 'https://eu.kith.com/account/addresses',
			'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7',
			'dnt': '1',
			'pragma': 'no-cache',
		}

		data = {
			"form_type": "customer_address",
			"utf8": "✓",
			"address[first_name]": self.profile['first_name'],
			"address[last_name]": self.profile['last_name'],
			"address[company]": "",
			"address[address1]": self.profile['address'],
			"address[address2]": "",
			"address[country]": self.profile['country'],
			"address[city]": self.profile['city'],
			"address[zip]": self.profile['zipCode'],
			"address[phone]": self.profile['phone'],
		}

		try:
			response = self.session.post('https://eu.kith.com/account/addresses', headers=headers, data=data, allow_redirects=False, proxies=self.proxy)
		except (requests.exceptions.ProxyError, requests.exceptions.ConnectionError):
			Logger.error(f"[{self.index}] Proxy Error... Rotating...")
			ProxyManager().banProxy(self.proxy["https"])
			self.proxy = ProxyManager().getProxy()
			return self.setAddy()
			
		except Exception as error:
			Logger.error(f"[{self.index}] Uncatched error... {error}")
			return (0)

		if (response.status_code == 302):
			redirectURI = response.headers['Location']

			if ("challenge" in redirectURI):
				Logger.error(f"[{self.index}] Rotating Proxy...")
				ProxyManager().banProxy(self.proxy["https"])
				self.proxy = ProxyManager().getProxy()
				return self.setAddy()

			if ("login" in redirectURI):
				return (-1)
			
			if (redirectURI == "https://eu.kith.com/account/addresses"):
				return (1)
		return (0)