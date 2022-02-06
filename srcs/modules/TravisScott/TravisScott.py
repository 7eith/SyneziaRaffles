'''

[ThePlayOffs] ThePlayOffs.py

Author: seith <seith.corp@gmail.com>

Created: 11/04/2021 20:09:22 by seith
Updated: 11/04/2021 20:09:22 by seith

Synezia Corp. (c) 2021 - MIT

'''

import PyInquirer
from singleton import Instance

from utils.cli_utils import printHeader
from utils.colors import Color
from logger.logger import Logger

import time

class TravisScott():
	def promptModule(self):
		moduleNames = [
			"Enter Raffle"
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

		if ("Enter" in answer):
			from .raffle import RaffleModule

			return RaffleModule()
		

		Logger.error("No available at this time.")
		return self.promptModule()

	def __init__(self):
		Instance().updateRPC("Running Travis Scott.")
		printHeader()

		"""
			Prompt Action
		"""

		self.promptModule()