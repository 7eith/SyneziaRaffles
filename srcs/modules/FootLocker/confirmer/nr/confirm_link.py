'''

[flx] confirm_link.py

Author: seith <seith.corp@gmail.com>

Created: 13/04/2021 02:10:24 by seith
Updated: 13/04/2021 02:10:24 by seith

Synezia Corp. (c) 2021 - MIT

'''

import requests
import json 

from logger.logger import Logger
from ..utils import flx_GetActivationLink, ExtractActivationTokenFromLink

class ConfirmLink():

	def __init__(self, index, link, userAgent):
		""" Values """
		self.index = index
		self.link = link
		self.profile = dict()
		self.userAgent = userAgent
		self.success = False
	
		# activationLink = flx_GetActivationLink(link)
		try:
			activationToken = ExtractActivationTokenFromLink(link)
		except Exception as error:
			Logger.error(f"[{index}] Invalid link.. ")
			self.success = False
			self.state = "INVALID"
			return 

		confirmStatus: int = self.confirmLink(activationToken)

		if (confirmStatus == 1):
			Logger.success(f"[{self.index}] Successfully confirmed!")
			self.success = True
			self.state = "SUCCESS"
		elif (confirmStatus == 2):
			Logger.warning(f"[{self.index}] Already confirmed!")
			self.success = True
			self.state = "CONFIRMED"
		elif (confirmStatus == -2):
			self.success = False
			self.state = "INVALID"
			Logger.error(f"[{self.index}] Invalid Token...")
		else:
			self.state = "FAILED"
			self.success = False
			Logger.error(f"[{self.index}] Failed to confirm..")


	def confirmLink(self, activationToken):
		headers = {
			'user-agent': self.userAgent,
			'content-type': 'application/json',
		}

		jsonData = {
			"activationToken": activationToken
		}

		data = json.dumps(jsonData, separators=(",", ":"))

		try:
			response = requests.post('https://www.footlocker.fr/api/v2/activation', headers=headers, data=data)

			""" Already Confirmed """
			if (response.json()['activationStatus'] == "userActivated"):
				self.profile['email'] = "X"
				self.profile['first_name'] = "X"
				self.profile['last_name'] = "X"
				return (2)

			if (response.json()['activationStatus'] == "tokenInvalid"):
				return (-2)

			self.profile['email'] = response.json()['userId'].split('|')[0]
			self.profile['first_name'] = response.json()['firstName']
			self.profile['last_name'] = response.json()['lastName']
			return (1)
		except Exception as error:
			Logger.error(error)
			return (-1)