"""

[proxy] controller.py

Author: seith <seith.corp@gmail.com>

Created: 06/02/2021 22:31:34 by seith
Updated: 06/02/2021 22:31:34 by seith

Synezia Corp. (c) 2021 - MIT

"""

from .config_singleton import ConfigurationSingletonMeta
from logger.logger import Logger

import inquirer
import glob
import csv
import os
import random
import json

from initer import Initer

configFile = "settings/settings.json"

class Configuration(metaclass=ConfigurationSingletonMeta):
	def __readConfigurationFile(self):

		try:
			_f = open(configFile, "r", encoding="utf-8", newline="")
		except FileNotFoundError as exception:
			Logger.info("[Info] Configuration not found. Creating new one!")

			os.mkdir("settings")

			with open(configFile, "w") as SettingsFile:
				SettingsFile.write(json.dumps(self.emptyConfig, indent=4))

			Initer().firstRun()
			return

		try:
			settings = json.load(_f)
		except Exception as error:
			Logger.error("An error has occured when trying to read settings.json")
			Logger.error(f"{error}")
			exit(-1)

		if len(settings) != len(self.emptyConfig):
			Logger.error(
				"Your current settings is missing a line. Please check it or delete it to recreate it clean!"
			)
			exit(-1)

		self.key = settings["key"]
		self.two_captcha = settings["two_captcha"]
		self.discord_webhook = settings["discord_webhook"]
		self.proxyless = settings["proxyless"]

	def __init__(self):
		self.emptyConfig = {
			"key": "DROP YOUR KEY HERE",
			"two_captcha": "2CAPTCHA KEY",
			"discord_webhook": "DISCORD_WEBHOOKS",
			"proxyless": "True"
		}

		self.key = ""
		self.two_captcha = ""
		self.discord_webhook = ""
		self.proxyless = True

		if (len(self.key) == 0):
			self.__readConfigurationFile()

	def getWebhookURL(self):
		return self.discord_webhook

	def getLicenseKey(self):
		return self.key