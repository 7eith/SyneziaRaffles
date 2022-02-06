'''

[Patta] patta.py

Author: seith <seith.corp@gmail.com>

Created: 26/02/2021 11:24:22 by seith
Updated: 26/02/2021 11:24:22 by seith

Synezia Corp. (c) 2021 - MIT

'''

from utils.cli_utils import printHeader, printLine
from utils.colors import Color

from logger.logger import Logger

from .account_create import AccountCreater
from .enter_raffle import PattaRaffle

from random_user_agent.user_agent import UserAgent
user_agent_rotator = UserAgent(software_names=['chrome', 'edge', 'opera', 'firefox', 'android-browser'], operating_systems=['windows', 'linux', 'macos', 'android', 'ios'])

class Patta():

	def __init__(self):
		self.version = '0.0.1'

		printHeader()

		print("==================================================================\n")
		print("\t\t* Welcome to Patta module")
		print("\t\t* Note(s): Module in Alpha mode...")
		print("\t\t* version {} - Northern Light\n".format(self.version))
		print("==================================================================\n")

		"""
			Create Logger File
		"""
		
		print('1. Create account')
		print('2. Enter raffle')
		res = input('What action to do? ')
		script = res[0]

		if (script == '1'):
			AccountCreater()

		if (script == '2'):
			PattaRaffle()