'''

[MicrosoftForm] enter_forn.py

Author: seith <seith.corp@gmail.com>

Created: 23/04/2021 05:28:03 by seith
Updated: 23/04/2021 05:28:03 by seith

Synezia Corp. (c) 2021 - MIT

'''

import time
import random
import requests
import datetime
import json
import re

from logger.logger import Logger

class EnterForm():

	def __init__(self, index, profile, formSettings, userAgent):

		Logger.info(f"[{index}] Starting Task ")
		self.index = index
		self.profile = profile
		self.formSettings = formSettings
		self.userAgent = userAgent

		""" Error Handlers """
		self.success = False
		self.status = "FAILED"

		""" Entry """
		if (self.scrap()):
			status: int = 0
			status = self.enterForm()

			if (status == 1):
				self.success = True
				self.status = "SUCCESS"
				Logger.success(f"[{index}] Successfully filled form!")
			else:
				self.success = False
				self.status = "FAILED"
				Logger.error(f"[{self.index}] Failed to entry into form!")
		else:
			self.success = False
			self.status = "FAILED"
			Logger.error(f"[{self.index}] Failed to Scrap form...")

	def scrap(self):
		Logger.info(f"[{self.index}] Scrapping form...")

		headers = {
			'authority': 'docs.google.com',
			'cache-control': 'max-age=0',
			'upgrade-insecure-requests': '1',
			'user-agent': self.userAgent,
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'sec-fetch-site': 'same-origin',
			'sec-fetch-mode': 'navigate',
			'sec-fetch-user': '?1',
			'sec-fetch-dest': 'document',
			'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7',
			'dnt': '1',
		}

		try:
			response = requests.get('https://docs.google.com/forms/d/e/1FAIpQLSehlz0N0kZfM8h9E-BPHJ1VYHpIkM_2pJuB3vvPmhZVB5aznw/viewform', headers=headers)
			self.resId = re.search('name="fbzx" value="(.+?)">', response.text).group(1)

			return (1)
		except:
			return (0)
		Logger.success(f"[{self.index}] Successfully scrapped form!")


	def prepareAnswers(self):
		data = dict()

		for index, key in enumerate(self.profile.keys()):
			if (str(key).startswith("entry")):
				data[key] = self.profile[key]

		if ("email" in self.profile):
			data['emailAddress'] = self.profile['email']
		if ("captcha" in self.profile):
			data['g-recaptcha-response'] = ""
		if ("receipt" in self.profile):
			print("OK")
		# data['emailReceipt'] = ''
		# data['g-recaptcha-response'] = ''
		data['fvv'] = '1'
		data['draftResponse'] = f'[null,null,"{self.resId}"]\r\n'
		data['pageHistory'] = '0'
		data['fbzx'] = str(self.resId)
		return (data)

	def enterForm(self):

		referer = f"{self.formSettings['url']}?fbzx={self.resId}" 

		headers = {
			'authority': 'docs.google.com',
			'cache-control': 'max-age=0',
			'upgrade-insecure-requests': '1',
			'origin': 'https://docs.google.com',
			'content-type': 'application/x-www-form-urlencoded',
			'user-agent': self.userAgent,
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'sec-fetch-site': 'same-origin',
			'sec-fetch-mode': 'navigate',
			'sec-fetch-user': '?1',
			'sec-fetch-dest': 'document',
			'referer': 'https://docs.google.com/forms/d/e/1FAIpQLSehlz0N0kZfM8h9E-BPHJ1VYHpIkM_2pJuB3vvPmhZVB5aznw/viewform?fbzx=-5496254235445302869',
			'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7',
			'dnt': '1',
		}

		data = self.prepareAnswers()

		try:
			response = requests.post(self.formSettings['formPostURL'], headers=headers, data=data)
			f = open("gfor.html", "w")
			f.write(response.text)
			f.close()
		except Exception as error:
			Logger.error(f"[{self.index}] Error has occured... {error}")
			return (0)

		if ("freebirdFormviewerViewResponseConfirmationMessage" in response.text):
			return (1)
		else:
			return (0)