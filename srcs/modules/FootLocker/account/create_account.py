'''

[account] create_account.py

Author: seith <seith.corp@gmail.com>

Created: 15/03/2021 21:27:52 by seith
Updated: 15/03/2021 21:27:52 by seith

Synezia Corp. (c) 2021 - MIT

'''

import requests
import json
import random
import time
import datetime

from logger.logger import Logger
from proxy.controller import ProxyManager
from controller.profile_parser import fetchProfiles

def get_random_date():

	# try to get a date
	try:
		date = datetime.datetime.strptime('{} {}'.format(random.randint(1, 366), random.randint(1990, 2003)), '%j %Y')
		dateSplit = str(date).split(' ')[0]

		parsed = dateSplit.split('-')
		text = parsed[1] + '/' + parsed[2] + '/' + parsed[0]

		return text
	# if the value happens to be in the leap year range, try again
	except ValueError:
		get_random_date()

class CreateAccount():

	def __init__(self, index, profile, loggerFileName):
		Logger.info(f"[{index}] Starting creating {profile['email']}...")
		self.loggerFileName = loggerFileName
		self.profile = profile
		self.index = index

		if ('country' in profile):
			self.extensionCode = profile['country']
		else:
			self.extensionCode = 'fr'

		self.createAccount()

	def createAccount(self):
		accountProfile = {
			"birthday": get_random_date(),
			"firstName": self.profile["first_name"],
			"preferredLanguage": "en",
			"lastName": self.profile["last_name"],
			"uid": self.profile["email"],
			"password": self.profile["password"],
		}

		userRegister = json.dumps(accountProfile, separators=(",", ":"))

		while True:

			try:
				response = requests.post(
					"https://www.footlocker.{}/apigate/users".format(self.extensionCode),
					data=userRegister,
					# max_retries=50
				)

			except OSError as error:
				Logger.error(error)
				# Logger.error(f"[{self.index}] Proxy Error")
				# ProxyManager().banProxy(self.proxy["https"])
				# self.proxy = ProxyManager().getProxy()

			if (response.status_code == 403):
				Logger.error("Proxy Banned")
				return
				# ProxyManager().banProxy(self.proxy["https"])
				# self.proxy = ProxyManager().getProxy()
			
			elif (response.status_code == 503):
				Logger.error('Queue Online. Waiting 60s to retry!')
				time.sleep(60)

			elif "Backend" not in response.text and "Fastly error:" not in response.text and "UnexpectedEOFAtTarget" not in response.text:
				if (response.status_code == 201):
					csvLine = "CREATED,"
					csvLine += ",".join(self.profile.values())
					csvLine += "\n"

					Logger.success(f"[{self.index}] Successfully created {self.profile['email']}")
					f = open(self.loggerFileName, 'a')
					f.write(csvLine)
					f.close()

					break

				if ("11105" not in response.text):
					Logger.error(response.text)

				code = response.json()['errors'][0]['code']

				if (code == 11105): 
					csvLine = "REGISTERED,"
					csvLine += ",".join(self.profile.values())
					csvLine += "\n"

					Logger.error(f"[{self.index}] Error, {self.profile['email']} already registered into FootLocker.")
					f = open(self.loggerFileName, 'a')
					f.write(csvLine)
					f.close()
					
					break
