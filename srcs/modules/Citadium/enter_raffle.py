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

from logger.logger import Logger
from proxy.controller import ProxyManager
from requests_toolbelt import MultipartEncoder


class CitadiumEnterRaffle():

	def __init__(self, index, profile, raffle, userAgent):
		Logger.info(f"[{index}] Starting Task")
		self.index = index
		self.profile = profile
		self.raffle = raffle
		self.userAgent = userAgent

		""" Variables """
		self.proxy = ProxyManager().getProxy()
		self.session = requests.Session()
		self.success = False
		self.status = "FAILED"

		enterRaffleStatus = self.enterRaffle()

		if (enterRaffleStatus):
			Logger.success(f"[{self.index}] Successfully entered")
			self.success = True
			self.status = "SUCCESS"
			return 
		else:
			Logger.error(f"[{self.index}] Error has occured when registering...")
			self.success = False
			self.status = "FAILED"

	def initSession(self):
		headers = {
			'Connection': 'keep-alive',
			'Cache-Control': 'max-age=0',
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': self.userAgent,
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7',
			'dnt': '1',
		}

		try:
			response = self.session.get('http://rsms.co/4E50', headers=headers, proxies=self.proxy, verify=False)
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
			headers = {
				'Connection': 'keep-alive',
				'Accept': '*/*',
				'X-Requested-With': 'XMLHttpRequest',
				'User-Agent': self.userAgent,
				'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
				'Origin': 'http://rsms.co',
				'Referer': 'http://rsms.co/4E50',
				'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7',
				'dnt': '1',
			}

			data = {
				'campaign_id': 'aa1eacc5-592d-46cd-8915-bcca1369514c',
				'csv_name': 'raffle',
				'fields': 'msisdn,firstname,lastname,pointure,codePostal, phone',
				'msisdn': '33623461075',
				'firstname': self.profile['firstname'],
				'lastname': self.profile['lastname'],
				'pointure': self.profile['size'],
				'codePostal': self.profile['departement'],
				'phone': self.profile['phone']
			}

			try:
				response = self.session.post('http://rsms.co/logics/commons/form/post-on-csv', headers=headers, data=data, verify=False, proxies=self.proxy)
			except (requests.exceptions.ProxyError, requests.exceptions.ConnectionError):
				Logger.error(f"[{self.index}] Proxy Error... Rotating...")
				ProxyManager().banProxy(self.proxy["https"])
				self.proxy = ProxyManager().getProxy()
				return self.enterRaffle()
				
			except Exception as error:
				Logger.error(f"[{self.index}] Uncatched error... {error}")
				return (False)

			try:
				if (response.json()['success'] == True):
					return (True)
			except Exception as error:
				return (False)

			return (False)