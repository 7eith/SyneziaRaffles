'''

[tools] ftl_tools.py

Author: seith <seith.corp@gmail.com>

Created: 15/02/2021 19:33:23 by seith
Updated: 15/02/2021 19:33:23 by seith

Synezia Corp. (c) 2021 - MIT

'''

from utils.colors import Color
from logger.logger import Logger

import random
import string
import itertools

class FootLockerTools():

	def __init__(self):
		self.createProfileFile()

	def createProfileFile(self):
		fileName = input(f"\n[{Color.BLUE}?{Color.RESET}] Name of the output files? \n-> ")
		res = input(f"\n[{Color.BLUE}?{Color.RESET}] How many profiles you want? \n-> ")
		
		try: 
			ProfileLength = int(res)
		except ValueError:
			Logger.error('Invalid number...')

		res = input(f"\n[{Color.BLUE}?{Color.RESET}] Max letters? \n-> ")
		try: 
			MaxLetters = int(res)
		except ValueError:
			Logger.error('Invalid number...')

		res = input(f"\n[{Color.BLUE}?{Color.RESET}] Start point? \n-> ")
		try: 
			StartPoint = int(res)
		except ValueError:
			Logger.error('Invalid number...')

		firstName = input(f"\n[{Color.BLUE}?{Color.RESET}] First Name? \n-> ")
		lastName = input(f"\n[{Color.BLUE}?{Color.RESET}] Last Name? \n-> ")
		password = input(f"\n[{Color.BLUE}?{Color.RESET}] Password? \n-> ")
		domain = input(f"\n[{Color.BLUE}?{Color.RESET}] CatchAll domain name? (ex: synezia.com) \n-> ")
		country = input(f"\n[{Color.BLUE}?{Color.RESET}] Country Code? (ex: fr)\n-> ")

		Logger.info('Generating lists...')

		all_combos = list(itertools.permutations(string.ascii_lowercase + string.digits, MaxLetters)) 
		all_combos = [''.join(combo) for combo in all_combos]

		if (len(all_combos) - StartPoint < ProfileLength):
			Logger.error('Cant generate too many requested emails with this length please increase it.')
			return self.createProfileFile()

		all_combos = all_combos[StartPoint:]
		results = list(itertools.islice(all_combos, ProfileLength))
		results = [sub + '@' + domain for sub in results] 

		Logger.success('Lists generated!')
		# print(results)

		with open('outputs/{}.csv'.format(fileName), 'w') as f:
			f.write(f"first_name,last_name,email,password,country\n")

			for item in results:
				f.write(f"{firstName},{lastName},{item},{password},{country}\n")

		