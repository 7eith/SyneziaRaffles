'''

[MicrosoftForm] form_module.py

Author: seith <seith.corp@gmail.com>

Created: 23/04/2021 05:01:14 by seith
Updated: 23/04/2021 05:01:14 by seith

Synezia Corp. (c) 2021 - MIT

'''

import PyInquirer
import time
import os
import requests
import re
import random

import utilities

from singleton import Instance
from profiles import Profile

from configuration.configuration import Configuration
from utils.cli_utils import printHeader
from utils.colors import Color
from logger.logger import Logger

from proxy.controller import ProxyManager

from .enter_form import EnterForm

from bs4 import BeautifulSoup

from notifier import NotifyFilledForm

class URLValidator(PyInquirer.Validator):
	def validate(self, document):
		if (not str(document.text).startswith("https://forms.office.com/Pages/ResponsePage.aspx?id=")):
			raise PyInquirer.ValidationError(
				message='Please enter a Microsoft Form URL',
				cursor_position=len(document.text))  # Move cursor to end

class DelayValidator(PyInquirer.Validator):
	def validate(self, document):
		values = document.text.split(",")
		
		if (len(values) != 2):
			raise PyInquirer.ValidationError(
				message='Enter a delay in seconds like : 5, 45 (Must be an Number separated by comma)',
				cursor_position=len(document.text))  # Move cursor to end

		try:
			min = int(values[0])
			max = int(values[1])
		except ValueError:
			raise PyInquirer.ValidationError(
				message='Enter a delay in seconds like : 5, 45 (Must be an Number separated by comma)',
				cursor_position=len(document.text))  # Move cursor to end

class MicrosoftForm():

	def __successTask(self, index, profile, state, formSettings, speed):
		try:
			f = open(self.loggerFileName, 'a')
			csvLine = f"{state},"
			csvLine += ",".join(profile.values())
			f.write(f"{csvLine}\n")
			f.close()
		except Exception as error:
			Logger.error(error)

		if (state == "SUCCESS"):
			NotifyFilledForm(profile, formSettings['url'], formSettings['title'], speed)

	def __failTask(self, index, profile, state):
		try:
			f = open(self.loggerFileName, 'a')
			csvLine = f"{state},"
			csvLine += ",".join(profile.values())
			f.write(f"{csvLine}\n")
			f.close()
		except Exception as error:
			Logger.error(error)

	def __getFormSettings(self):
		formId = self.url.split('id=')[1]

		try:
			response = requests.get(self.url)

			formURLMatcher = re.search('prefetchFormUrl: "(.+?)/light', response.text)
			formURL = formURLMatcher.group(1)

			soup = BeautifulSoup(response.text, 'html.parser')
			title = soup.find('title').string.strip()
		except Exception as error:
			Logger.error(f"Failed to fetch form settings.. {error}")
			return
		
		formURL += "/forms(%27"
		formURL += formId
		formURL += "%27)/responses"

		formSettings = {
			"url": self.url,
			"id": formId,
			"formPostURL": formURL,
			"title": title
		}

		return (formSettings)

	def __promptSettings(self):
		questions = [
			{
				'type': 'input',
				'name': 'url',
				'message': 'Enter form URL',
				'validate': URLValidator,
			},
		]

		url = (
			PyInquirer.prompt(questions=questions, keyboard_interrupt_msg=f"Cancelled by User. Exiting CLI")
			.get("url")
		)

		if (not url):
			exit(0)

		self.url = url

		questions = [
			{
				'type': 'input',
				'name': 'size',
				'message': 'Enter delay in seconds here (Separated by swoosh like 1,5)',
				'default': '5, 45',
				'validate': DelayValidator
			},
		]

		answer = (
			PyInquirer.prompt(questions=questions, keyboard_interrupt_msg=f"Cancelled by User. Exiting CLI")
			.get("size")
		)

		delayAnswer = answer.split(",")

		self.minDelay = int(delayAnswer[0])
		self.maxDelay = int(delayAnswer[1])

	def __createLogger(self, loggerFileName, example_profile):
		header = "status," + ",".join(example_profile.keys())

		try:
			f = open(loggerFileName, 'w')
			f.write(f"{header}\n")
			f.close()
		except Exception as error:
			Logger.error(error)

	def __init__(self):
		moduleName = "MicrosoftForm"
		action = "Enter"
		version = "0.0.1"
		date = Instance().getDate()
		self.loggerFileName = f"logs/{moduleName}/{action}_{date}.csv"

		""" UI """
		printHeader()
		Instance().updateRPC(f"Running Raffle...")
		utilities.setTitle(f"SyneziaRaffle - Running custom MicrosoftForm")
		
		""" Status """
		successTask: int = 0
		failedTask: int = 0

		""" Proxies """
		if (not Configuration().proxyless):
			proxies = ProxyManager(moduleName)

		""" Profiles """
		profile = Profile(moduleName)
		profiles = profile.fetchProfiles()

		profileName = os.path.basename(profile.profileFile).split('.')[0]
		profileLen = len(profiles)

		self.__promptSettings()

		""" Assets """
		Logger.info("Initializating assets...")

		from random_user_agent.user_agent import UserAgent
		user_agent_rotator = UserAgent(software_names=['chrome', 'edge', 'opera', 'firefox'], operating_systems=['windows', 'linux', 'macos'])
		self.__createLogger(self.loggerFileName, profiles[0])

		""" Extract Form Settings """
		formSettings = self.__getFormSettings()

		""" Resume """
		utilities.printHeader()
		utilities.printLine()
		Logger.info("\t\t     [Resume]")
		Logger.info(">> Profile: {} [{}]".format(profile.profileFile, len(profiles)))
		if (not Configuration().proxyless):
			Logger.info(">> Proxies: {} [{}]".format(proxies.proxiesFile, len(proxies.getProxies())))
		Logger.info(">> Log File: {}".format(f"{action}_{date}.csv"))
		Logger.info(">> Form: {}".format(self.url))
		Logger.info(">> Delay: {} - {}\n".format(self.minDelay, self.maxDelay))

		for index, profile in enumerate(profiles):
			print("")
			utilities.printLine()

			task = EnterForm(index, profile, formSettings, user_agent_rotator.get_random_user_agent())

			if (task.success):
				successTask += 1
				self.__successTask(index, profile, task.status, formSettings, task.solveTime)
				
			else:
				failedTask += 1
				self.__failTask(index, profile, task.status)		

			remaining = profileLen - (index + 1)
			utilities.setTitle(f"SyneziaRaffle - / Success: {str(successTask)} - Failed {str(failedTask)} - Remaining {str(remaining)}")
			
			delay = random.randint(self.minDelay, self.maxDelay)
			Logger.info(f"Waiting {delay} to do another Task...")
			time.sleep(delay)	

			