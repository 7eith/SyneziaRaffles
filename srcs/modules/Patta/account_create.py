'''

[Patta] account_create.py

Author: seith <seith.corp@gmail.com>

Created: 26/02/2021 13:10:47 by seith
Updated: 26/02/2021 13:10:47 by seith

Synezia Corp. (c) 2021 - MIT

'''

import requests

from utils.cli_utils import printHeader, printLine
from utils.colors import Color

from logger.logger import Logger
from proxy.controller import ProxyManager
from controller.profile_parser import fetchProfiles

from random_user_agent.user_agent import UserAgent
user_agent_rotator = UserAgent(software_names=['chrome', 'edge', 'opera', 'firefox', 'android-browser'], operating_systems=['windows', 'linux', 'macos', 'android', 'ios'])

class AccountCreater():

	def __init__(self):
		self.proxyManager = ProxyManager()
		self.profiles = fetchProfiles("Patta")

		self.createAccount(self.profiles[0])

	def createAccount(self, profile):
		Logger.info('[Patta] Creating Account...')
		print(profile)

		proxy = self.proxyManager.getProxy()
		userAgent = user_agent_rotator.get_random_user_agent()
		session = requests.Session()

		headers = {
			'Host': 'www.patta.nl',
			'cache-control': 'no-cache',
			'upgrade-insecure-requests': '1',
			'origin': 'https://www.patta.nl',
			'content-type': 'application/x-www-form-urlencoded',
			'user-agent': userAgent,
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'sec-fetch-site': 'same-origin',
			'sec-fetch-mode': 'navigate',
			'sec-fetch-user': '?1',
			'sec-fetch-dest': 'document',
			'referer': 'https://www.patta.nl/account/register',
			'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7',
			'dnt': '1',
			'pragma': 'no-cache',
		}

		data = 'form_type=create_customer&utf8=%E2%9C%93' 
		data += '&customer%5Bfirst_name%5D=' 
		data += profile['name']
		data += '&customer%5Blast_name%5D=' 
		data += profile['surname']
		data += '&customer%5Bemail%5D=' 
		data += profile['email']
		data += '&customer%5Bpassword%5D=' 
		data += profile['password']

		response = requests.post('https://www.patta.nl/account', headers=headers, data=data, proxies=proxy)
		print(response.text)
		print(response.status_code)

