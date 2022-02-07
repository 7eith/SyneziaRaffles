"""

[FootLocker] ftl_raffle.py

Author: seith <seith.corp@gmail.com>

Created: 27/01/2021 21:16:17 by seith
Updated: 27/01/2021 21:16:17 by seith

Synezia Corp. (c) 2021 - MIT

"""

import requests
import json
import inquirer
import glob
import random

from utils.cli_utils import printHeader, printLine
from controller.profile_parser import fetchProfiles
from controller.proxies_parser import fetchProxies

from .raffles.ftl_raffles_module import FootLockerRaffleModule
from .checker.ftl_checker_module import FootLockerCheckerModule
from .account.ftl_account_module import FootLockerAccountCreaterModule

from notifier.discord import DiscordNotifier
from .tools.ftl_tools import FootLockerTools

from singleton.controller import Instance

availableActions = [
	"Create Account",
	"Enter raffle",
	"Check wins",
	"Confirm wins",
	"Tools"
]

class FootLocker:
	def promptMenu(self):
		questions = [
			inquirer.List(
				"choice",
				message="What action do you want to run?",
				choices=availableActions,
			),
		]

		answers = inquirer.prompt(questions)

		if answers:
			return answers.get("choice").strip().lower()
		else:
			sys.exit(1)

	def __init__(self):
		self.session = requests.Session()
		self.version = "0.0.3"
		
		"""
			UI
		"""

		printHeader()
		print("==================================================================\n")
		print("\t\t* Welcome to FootLocker module")
		print("\t\t* Note(s): Module in Alpha mode...")
		print("\t\t* version {} - Northern Light\n".format(self.version))
		print("==================================================================\n")

		"""
			Prompt
		"""

		res = self.promptMenu()

		if "create" in res:
			printHeader()
			printLine()
			FootLockerAccountCreaterModule()

		if "enter" in res:
			printHeader()
			printLine()
			FootLockerRaffleModule()

		if "tools" in res:
			printHeader()
			printLine()
			FootLockerTools()

		if "check" in res:
			printHeader()
			printLine()
			FootLockerCheckerModule()
