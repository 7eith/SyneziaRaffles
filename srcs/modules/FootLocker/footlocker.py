'''

[FuckFTL] footlocker.py

Author: seith <seith.corp@gmail.com>

Created: 15/03/2021 00:29:01 by seith
Updated: 15/03/2021 00:29:01 by seith

Synezia Corp. (c) 2021 - MIT

'''

import PyInquirer
from singleton import Instance

from utils.cli_utils import printHeader
from utils.colors import Color
from logger.logger import Logger

class FootLocker():
	def promptModule(self):
		moduleNames = [
			"Create Account",
			"Confirm Accounts",
			"Enter Raffle",
			"Check Results",
			"Confirm win",
			"[Tools] Generate CSVs",
			PyInquirer.Separator(), 
			"Return"
		]

		questions = [
			{
				'type': 'list',
				'name': 'choice',
				'message': 'Select a module to Run',
				'choices': moduleNames	
			}
		]

		answer = (
			PyInquirer.prompt(questions=questions, keyboard_interrupt_msg=f"{Color.RED}Cancelled by User. Exiting CLI{Color.RESET}")
			.get("choice")
		)

		if not answer:
			exit(0)

		if "Create" in answer:
			from .comptes import AccountModule

			return AccountModule()

		# if "Enter" in answer:
		# 	from .sessions import SessionModule

		# 	return SessionModule()
		if "Generate" in answer:
			from .tools import FootLockerTools

			FootLockerTools()
			return self.promptModule()

		if "Confirm Accounts" in answer:
			from .confirmer import FootLockerConfirmer

			return FootLockerConfirmer()

		Logger.error("No available at this time. Please wait :)")
		return self.promptModule()

	def __init__(self):
		Instance().updateRPC("Running FootLocker.")
		printHeader()

		"""
			Prompt Action
		"""

		self.promptModule()