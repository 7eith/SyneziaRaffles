'''

[TheBrokenArm] tba_module.py

Author: seith <seith.corp@gmail.com>

Created: 16/02/2021 18:48:44 by seith
Updated: 16/02/2021 18:48:44 by seith

Synezia Corp. (c) 2021 - MIT

'''

from utils.cli_utils import printHeader, printLine
from utils.colors import Color

from logger.logger import Logger
from proxy.controller import ProxyManager
from controller.profile_parser import fetchProfiles

import requests
import random,string
import time

from .fp_logger import logSuccessEntry, logFailedEntry

from random_user_agent.user_agent import UserAgent
user_agent_rotator = UserAgent(software_names=['chrome', 'edge', 'opera', 'firefox', 'android-browser'], operating_systems=['windows', 'linux', 'macos', 'android', 'ios'])


currentScripts = {
	f'{Color.BLUE}Enter raffle': 'enter',
}

class FootPatrolModule():

	def __promptMenu(self):
		res = input(f"\n[{Color.BLUE}?{Color.RESET}] How many delays in seconds separated by swoosh (Example 0,60) ?\n-> ")

		SplittedAnswer = res.split(",")

		if len(SplittedAnswer) != 2:
			Logger.error("Error, please use: MIN DELAYS, MAX DELAYS")
			return self.__promptMenu()

		try:
			min = float(SplittedAnswer[0])
			max = float(SplittedAnswer[1])
		except ValueError:
			Logger.error('Failed to get delays, please retry')
			return self.__promptMenu()

		self.minDelay = min
		self.maxDelay = max

	def __init__(self):
		self.version = '0.0.1'

		printHeader()

		print("==================================================================\n")
		print("\t\t* Welcome to FootPatrol module")
		print("\t\t* Note(s): Module in Alpha mode...")
		print("\t\t* version {} - Northern Light\n".format(self.version))
		print("==================================================================\n")

		self.proxyManager = ProxyManager("FootPatrol")
		self.proxy = self.proxyManager.getProxy()

		profiles = fetchProfiles("FootPatrol")
		self.__promptMenu()

		"""
			Create Logger File
		"""

		f = open('logs/fp_entry.csv', 'a')
		f.write("status,first_name,last_name,email")
		f.close()

		for i, profile in enumerate(profiles):
			Logger.info(f"[{i}] Entering into raffle {profile['email']}...")
			self.enterRaffle(i, profile)
			waitingTime = random.randint(self.minDelay, self.maxDelay)
			Logger.info(f"Waiting delays for new entry... {waitingTime}s.")
			time.sleep(waitingTime)

	def enterRaffle(self, i, profile):
		headers = {
			'Referer': 'https://footpatrol.s3.amazonaws.com/',
			'User-Agent': user_agent_rotator.get_random_user_agent(),
		}

		params = (
			('nourl', 'UK_NIKE'),
			('firstName', f"{profile['first_name']} {profile['last_name']}"),
			('email', profile['email']),
			('telephone', profile['telephone']),
			('UK_NIKE_shoetype', 'Califia'),
			('UK_NIKE_shoesize', profile['size']),
			('UK_NIKE_cityofres', profile['city']),
			('yzemail', 'UK_NIKE'),
			('UK_NIKE_countryofres', profile['country']),
			('emailpermit', '1'),
			# ('agepermit', 'Y'),
			('sms_optout', '0'),
			('site', 'FP'),
			('currency', 'GBP'),
		)

		try :
			res = requests.get("https://redeye.footpatrol.com/cgi-bin/rr/blank.gif", headers=headers, params=params, proxies=self.proxyManager.getProxy())
		except Exception as error:
			Logger.error('Error has occured..')
			Logger.error(error)
			logFailedEntry(i, profile)
			return

		logSuccessEntry(i, profile)
