'''

[license] License.py

Author: seith <seith.corp@gmail.com>

Created: 11/02/2021 15:51:22 by seith
Updated: 11/02/2021 15:51:22 by seith

Synezia Corp. (c) 2021 - MIT

'''

import requests
import json
import uuid 
import sys
import os
import time

import threading
import time

import utilities

from singleton import Instance

from logger.logger import Logger
from configuration.configuration import Configuration

class Licenser():

	def __init__(self):
		Logger.info(f'* Checking License Key!')

		self.key = Configuration().getLicenseKey()
		self.machineId = hex(uuid.getnode())
		self.apiEndpoint = "http://51.68.44.206:8080/auth"

		profile = {
			"key": self.key,
			"machineId": self.machineId
		}

		try :
			response = requests.post(self.apiEndpoint + '/verify', json=profile)
		except requests.ConnectionError:
			Logger.error('Server issues! Please contact an Admin on Discord.')

			try:
				time.sleep(5)
				sys.exit()
			except KeyboardInterrupt:
				Logger.error('Exiting NOW. (Asked by user)')
				sys.exit()
			
			return

		if (response.status_code != 200):
			Logger.error("Exiting CLI! Invalid Key! If you think its an error reset your key or contact staff!")
			Logger.error(f"Reason: {response.json()['message']}")

			try:
				time.sleep(5)
			except KeyboardInterrupt:
				Logger.error('Exiting NOW. (Asked by user)')
				sys.exit()

			sys.exit()

		self.profile = response.json()
		Instance().initProfile(self.profile)

		# thread = threading.Thread(target=self.heartBeat, args=())
		# thread.daemon = True
		# thread.start()  

	def heartBeat(self):
		

		while True:
			try :
				response = requests.get(f"{self.apiEndpoint}/heartbeat/{self.machineId}")
			except requests.ConnectionError:
				Logger.error('Server issues! Please contact an Admin on Discord.')
				time.sleep(20)
				os._exit(1)

			if (response.status_code != 200):
				Logger.error("What do you do? Dont try to reset ur key when you running. This incident will be log.")
				time.sleep(2)
				os._exit(1)

			time.sleep(60)