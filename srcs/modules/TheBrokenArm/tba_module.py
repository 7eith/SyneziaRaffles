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
import os
import random,string
import time
import cloudscraper
from bs4 import BeautifulSoup

from requests_toolbelt import MultipartEncoder
from .tba_logger import logSuccessEntry, logFailedEntry

from concurrent.futures import ThreadPoolExecutor, as_completed
from profiles import Profile



from random_user_agent.user_agent import UserAgent
user_agent_rotator = UserAgent(software_names=['chrome', 'edge', 'opera', 'firefox', 'android-browser'], operating_systems=['windows', 'linux', 'macos', 'android', 'ios'])

sizesAvailable = {
	"5 US",
	"5.5 US",
	"6 US",
	"6.5 US",
	"7 US",
	"7.5 US",
	"8 US",
	"8.5 US",
	"9 US",
	"9.5 US",
	"10 US",
	"10.5 US",
	"11 US",
	"11.5 US",
	"12 US",
	"12.5 US",
	"13 US"
	"13.5 US"
	"14 US"
	"14.5 US"
	"15 US"
}

class TBAModule():

	def __promptRaffle(self):
		# scraper = cloudscraper.create_scraper()
		# res = scraper.get('https://www.the-broken-arm.com/fr/content/12-raffle')
		# soup = BeautifulSoup(res.text, 'html5lib')

		# activeURISelector = soup.select('.elementor-widget-container > div > a')
		URIs = ["nike-fragment-x-dunk-hi"]

		# for uri in activeURISelector:
		# 	URIs.append(uri['href'].split('=')[1])

		
		for index, url in enumerate(URIs):
			print(f"{Color.BLUE}{index + 1}. {url}")
		print(Color.RESET)

		res = input("[?] Select a raffle to run! ")[0]

		try:
			raffleOffset = int(res)
			raffleOffset = raffleOffset - 1

			if (raffleOffset < 0 or raffleOffset + 1 > len(URIs)):
				raise ValueError
			
		except ValueError:
			Logger.error('Please select a live raffle!')
			return self.__promptRaffle()

		self.raffleId = URIs[raffleOffset]
		self.raffleURI = f"https://www.the-broken-arm.com/fr/raffle-store?color={self.raffleId}"

	def __promptDelay(self):
		res = input(f"\n[{Color.BLUE}?{Color.RESET}] How many delays in seconds separated by swoosh (Example 0,60) ?\n-> ")

		SplittedAnswer = res.split(",")

		if len(SplittedAnswer) != 2:
			Logger.error("Error, please use: MIN DELAYS, MAX DELAYS")
			return self.__promptDelay()

		try:
			min = float(SplittedAnswer[0])
			max = float(SplittedAnswer[1])
		except ValueError:
			Logger.error('Failed to get delays, please retry')
			return self.__promptDelay()

		self.minDelay = min
		self.maxDelay = max

	def __fetchSizes(self):
		scraper = cloudscraper.create_scraper()
		res = scraper.get(self.raffleURI)
		soup = BeautifulSoup(res.text, 'html5lib')
		sizesSelector = soup.select('#size > option')[1:]
		sizes = []

		for data in sizesSelector:
			sizeCollector = {
				"value": data.text,
				"size": data.text.split(' ')[0]
			}
			sizes.append(sizeCollector)

		self.sizes = sizes

	def __init__(self):
		self.version = '0.0.1'

		printHeader()

		print("==================================================================\n")
		print("\t\t* Welcome to TheBrokenArm module")
		print("\t\t* Note(s): Module in Alpha mode...")
		print("\t\t* version {} - Northern Light\n".format(self.version))
		print("==================================================================\n")

		self.proxyManager = ProxyManager("TheBrokenArm")
		self.proxy = self.proxyManager.getProxy()

		profile = Profile("TheBrokenArm")
		profiles = profile.fetchProfiles()
		profileName = os.path.basename(profile.profileFile).split('.')[0]
		profileLen = len(profiles)
		self.__promptDelay()
		self.__promptRaffle()
		# self.__fetchSizes()

		"""
			Create Logger File
		"""

		f = open('logs/tba_entry.csv', 'w')
		f.write("status,lastname,firstname,days,months,years,phone,email,country,size")
		f.close()

		# processes = []
		# with ThreadPoolExecutor(max_workers=2) as executor:
		# 	for index, profile in enumerate(profiles):
		# 		executor.submit(self.enterRaffle, index, profile)

		# Logger.info('Terminated! Good Luck')
		for i, profile in enumerate(profiles):

			Logger.info(f"[{i}] Entering into raffle {profile['email']}...")

			if (profile['size'] == 'RANDOM'):
				profile['size'] = random.choice(list(sizesAvailable))
				
			self.enterRaffle(i, profile)

			waitingTime = random.randint(self.minDelay, self.maxDelay)
			Logger.info(f"Waiting delays for new entry... {waitingTime}s.")
			time.sleep(waitingTime)

	def enterRaffle(self, i, profile):
		profile['country'] = "France"
		fields = {
			"lastname": profile['lastname'],
			"firstname": profile['firstname'],
			"days": profile['days'],
			"months": profile['months'],
			"years": profile['years'],
			"phone": profile['phone'],
			"email": profile['email'],
			"country": '8',
			"size": profile['size'],
			"gdpr_consent_chkbox": '1',
			"submitMessage": ''
		}

		boundary = '----WebKitFormBoundary' + ''.join(random.sample(string.ascii_letters + string.digits, 16))
		m = MultipartEncoder(fields=fields, boundary=boundary)

		headers = {
			'Host': 'www.the-broken-arm.com',
			'cache-control': 'no-cache',
			'upgrade-insecure-requests': '1',
			'origin': 'https://www.the-broken-arm.com',
			'content-type': m.content_type,
			'user-agent': user_agent_rotator.get_random_user_agent(),
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'sec-fetch-site': 'same-origin',
			'sec-fetch-mode': 'navigate',
			'sec-fetch-user': '?1',
			'sec-fetch-dest': 'document',
			'referer': "https://www.the-broken-arm.com/fr/raffle-store?color=nike-fragment-x-dunk-hi",
			'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7',
			'dnt': '1',
			'pragma': 'no-cache',
		}

		params = (
			('color', 'nike-fragment-x-dunk-hi'),
		)

		try :
			res = requests.post('https://www.the-broken-arm.com/fr/raffle-store', headers=headers, params=params, data=m, proxies=self.proxyManager.getProxy())
		except Exception as error:
			Logger.error('Error has occured..')
			Logger.error(error)
			return


		if ("error=already-registered" in res.text):
			Logger.error(f"[{i}] {profile['email']} already registered!")
			logFailedEntry(i, profile, self.raffleId)
			return

		# print(res.text)
	
		if ("Merci pour votre participation" in res.text):
			logSuccessEntry(i, profile, self.raffleId)
		else:
			logFailedEntry(i, profile, self.raffleId)
