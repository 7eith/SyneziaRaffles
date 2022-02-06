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

from logger.logger import Logger

class EnterForm():

	def __getFieldsNumber(self):
		occurency = 0
		for index, key in enumerate(self.profile.keys()):
			if (str(key).startswith("r")):
				occurency += 1
		return (occurency)

	def __parseTypeTime(self):
		type_time = self.profile['type_time'].split(':')

		try:
			minTime = int(type_time[0])
			maxTime = int(type_time[1])
		except ValueError:
			Logger.error("Invalid TypeTime (MIN_DELAY:MAX_DELAY)")
			return (None)

		solveTime = self.fieldsNumber * random.randint(minTime, maxTime)
		return (solveTime)

	def __setTimeline(self):
		submitedDatetime = datetime.datetime.now()
		self.submitDate = "{:02d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}.{:02d}Z".format(
			submitedDatetime.year,
			submitedDatetime.month,
			submitedDatetime.day,
			submitedDatetime.hour,
			submitedDatetime.minute,
			submitedDatetime.second,
			random.randint(0, 999),
		)

		startDateTime = submitedDatetime - datetime.timedelta(0, self.solveTime)
		self.startDate = "{:02d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}.{:02d}Z".format(
			startDateTime.year,
			startDateTime.month,
			startDateTime.day,
			startDateTime.hour,
			startDateTime.minute,
			startDateTime.second,
			random.randint(0, 999),
		)


	def __init__(self, index, profile, formSettings, userAgent):
		Logger.info(f"[{index}] Starting Task ")
		self.index = index
		self.profile = profile
		self.formSettings = formSettings
		self.userAgent = userAgent

		""" Error Handlers """
		self.success = False
		self.state = "FAILED"

		""" Chronos (Timeline Manager) """
		self.fieldsNumber = self.__getFieldsNumber()
		self.solveTime = self.__parseTypeTime()

		if (self.solveTime == None):
			self.success = False
			self.status = "INVALID"
			return (0)
		
		self.__setTimeline()

		""" Entry """
		status: int = self.enterForm()

		if (status == 1):
			self.success = True
			self.status = "SUCCESS"
			return 
		else:
			self.success = False
			self.status = "FAILED"

	def prepareAnswers(self):
		answersField = "["

		for index, key in enumerate(self.profile.keys()):
			if (str(key).startswith("r")):
				answersField += '{"questionId":"'
				answersField += key
				answersField += '","answer1":"'
				answersField += self.profile[key]
				answersField += '"}'

				self.fieldsNumber -= 1
				if (self.fieldsNumber != 0):
					answersField += ','

		answersField += "]"

		parameters = {
			"answers": answersField,
			"startDate": self.startDate,
			"submitDate": self.submitDate,
		}

		# print(parameters)
		# print('{"answers":"[{\\"questionId\\":\\"r906b0751500a4c31874c25605d83dd13\\",\\"answer1\\":\\"Madame\\"},{\\"questionId\\":\\"r14b10bcde1554f0682d0429afae3be27\\",\\"answer1\\":\\"s\\"},{\\"questionId\\":\\"r0f0669e6b2d9454ead76d7ba4aadbb9b\\",\\"answer1\\":\\"s\\"},{\\"questionId\\":\\"rbbfc490f38784e74a5735535f6511925\\",\\"answer1\\":\\"s\\"},{\\"questionId\\":\\"rf47f0582acd24bf7889626eca0c24c2e\\",\\"answer1\\":\\"Oui\\"},{\\"questionId\\":\\"r0c70d52ccee84f2696f5b6fd6b9f3e79\\",\\"answer1\\":\\"s\\"},{\\"questionId\\":\\"rd41c3b60f6004176bce99e7a98bf3351\\",\\"answer1\\":\\"2021-04-23\\"},{\\"questionId\\":\\"r6194c001327d4e82bf860351691d0f81\\",\\"answer1\\":\\"33333\\"},{\\"questionId\\":\\"r0ed23f37808146488cd2bf12cc3b0b16\\",\\"answer1\\":\\"Oui\\"},{\\"questionId\\":\\"rb7cb2de10309420bab6088b4ca752041\\",\\"answer1\\":\\"Dark iris\\"},{\\"questionId\\":\\"r08d2f4456744410ca5b9bd903ad343eb\\",\\"answer1\\":\\"40 - 7 US\\"}]","startDate":"2021-04-23T06:11:04.663Z","submitDate":"2021-04-23T06:11:21.317Z"}')
		return json.dumps(parameters, separators=(",", ":"))

	def enterForm(self):
		headers = {
			'authority': 'forms.office.com',
			'odata-version': '4.0',
			'x-ms-form-request-ring': 'msa',
			'authorization': '',
			'content-type': 'application/json',
			'accept': 'application/json',
			'odata-maxverion': '4.0',
			'user-agent': self.userAgent,
			'shareinvitationkey': 'undefined',
			'x-ms-form-request-source': 'ms-formweb',
			'origin': 'https://forms.office.com',
			'sec-fetch-site': 'same-origin',
			'sec-fetch-mode': 'cors',
			'sec-fetch-dest': 'empty',
			'referer': self.formSettings['url'],
			'accept-language': 'en-GB,en;q=0.9',
		}

		data = self.prepareAnswers()

		try:
			response = requests.post(self.formSettings['formPostURL'], headers=headers, data=data)
		except Exception as error:
			Logger.error(f"[{self.index}] Error has occured... {error}")
			return (0)
		
		if ("error" in response.json() and response.json()['error']):
			errorMessage = response.json()['error']['message']
			Logger.error(f"[{self.index}] {errorMessage}")
			return (0)

		if (response.status_code == 201):
			Logger.success(f"[{self.index}] Successfully filled form!")
			return (1)