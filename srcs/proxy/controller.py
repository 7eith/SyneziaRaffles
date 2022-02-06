"""

[proxy] controller.py

Author: seith <seith.corp@gmail.com>

Created: 06/02/2021 22:31:34 by seith
Updated: 06/02/2021 22:31:34 by seith

Synezia Corp. (c) 2021 - MIT

"""

from .proxy_singleton import ProxySingletonMeta
from logger.logger import Logger

import PyInquirer
import glob
import csv
import os
import random

from utils.colors import Color


class ProxyManager(metaclass=ProxySingletonMeta):
	def __read_proxies(self, proxies_file_name):
		_f = open(proxies_file_name, "r", encoding="utf-8", newline="")

		formatedProxies = []
		proxies = _f.readlines()
		for line in proxies:

			line = line.strip()
			line = line.split(":")
			formatedProxies.append(
				"http://" + line[2] + ":" + line[3] + "@" + line[0] + ":" + line[1]
			)

		return formatedProxies

	def __selectProxiesFile(self):

		if len(glob.glob(f"proxies/{self.moduleName}/*")) < 1:
			Logger.error('No proxies found in directory.')
			Logger.info(f"Put proxies in proxies/{self.moduleName}/ it's updating in live")

			try:
				input("[{}] Press Enter for retrying or exit CLI.".format(Logger.getTime()))
			except KeyboardInterrupt:
				return exit(0)
				
			return self.__selectProxiesFile()

		questions = [
			{
				'type': 'list',
				'name': 'choice',
				'message': 'Select a proxies file.',
				'choices': glob.glob(f"proxies/{self.moduleName}/*")
			}
		]

		answer = (
			PyInquirer.prompt(questions=questions, keyboard_interrupt_msg=f"{Color.RED}Cancelled by User. Exiting CLI{Color.RESET}")
			.get("choice")
		)

		if not answer:
			exit(0)

		return answer.strip()

	"""
		Constructor
	"""

	def __init__(self, moduleName):
		self.moduleName = moduleName
		file = self.__selectProxiesFile()

		Logger.info(f"Reading proxies from {file} ...")

		self.proxies = self.__read_proxies(os.getcwd() + "/" + file)
		self.currentProxy = self.getProxy()
		self.proxiesFile = file

		Logger.info(
			f"{len(list(self.proxies))} proxies successfully fetched from {file} !"
		)

	"""
		getProxy()
			return random proxy
	"""

	def getProxy(self):
		proxy = random.choice(self.proxies)

		return {"https": proxy, "http": proxy}

	def getProxies(self):
		return self.proxies

	def banProxy(self, proxy):
		# print('[Info] Removing {} from Proxies'.format(proxy))

		if proxy in self.proxies:
			self.proxies.remove(proxy)

		# print('[Info] Removed proxy from proxies list.')

	def getCurrentProxy(self):
		return self.currentProxy
