'''

[SM] StreetMachine.py

Author: seith <seith.corp@gmail.com>

Created: 03/04/2021 17:26:44 by seith
Updated: 03/04/2021 17:26:44 by seith

Synezia Corp. (c) 2021 - MIT

'''

import PyInquirer
from singleton import Instance

from utils.cli_utils import printHeader
from utils.colors import Color
from logger.logger import Logger

import time

class StreetMachine():
	def promptModule(self):
		moduleNames = [
			"Account Creator",
			"Enter Raffle",
			"AIO (Create then Enter)",
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

		if ("AIO" in answer):

			from .aio import AIOModule
			return AIOModule()

		if ("Account" in answer):

			from .account import AccountModule
			return AccountModule()

		if ("Raffle" in answer):

			from .raffle import RaffleModule
			return RaffleModule()

		Logger.error("No available at this time.")
		return self.promptModule()

	def __init__(self):
		Instance().updateRPC("Running StreetMachine.")
		printHeader()

		"""
			Prompt Action
		"""

		self.promptModule()