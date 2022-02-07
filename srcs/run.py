"""

[SyneziaSoft/CLI] run.py

Author: seith <seith.corp@gmail.com>

Created: 09/03/2021 00:14:49 by seith
Updated: 09/03/2021 00:14:49 by seith

Synezia Corp. (c) 2021 - MIT

"""

import PyInquirer
import os

from utils.cli_utils import printHeader, printLine
from configuration.configuration import Configuration
from logger.logger import Logger
from license.License import Licenser

from utils.colors import Color

from singleton import Instance

from ui import uiDefaultTheme

import utilities

class CLI:
	def promptModule(self):
		moduleNames = [
			"Travis Scott",
			"Courir",
			"Kith",
			"Naked",
			"FootLocker App",
			"Solebox",
			"StreetMachine",
			"ThePlayOffs",
			"Impact",
			"Citadium",
			"TheBrokenArm",
			PyInquirer.Separator(f"\n     --- AIO ---"),
			"Google Form",
			"Microsoft Form"
		]

		questions = [
			{
				"qmark": "[?]",
				"type": "list",
				"name": "choice",
				"message": "Select a module to use",
				"choices": moduleNames,
			}
		]

		answer = PyInquirer.prompt(
			questions=questions,
			keyboard_interrupt_msg=f"{Color.RED}Cancelled by User. Exiting CLI{Color.RESET}",
			# true_color=True,
			style=uiDefaultTheme,
		).get("choice")

		if not answer:
			exit(0)

		if "Impact" in answer:
			from modules.Impact import ImpactRaffle

			ImpactRaffle()
			
		if "Citadium" in answer: 
			from modules.Citadium import Citadium

			Citadium()
		if "Google" in answer:
			from modules.GoogleForm import GoogleForm

			GoogleForm()
		if "Kith" in answer:
			from modules.Kith import Kith

			Kith()

		if "TheBrokenArm" in answer:
			from modules.TheBrokenArm.tba_module import TBAModule

			TBAModule()

		if "Naked" in answer:
			from modules.Naked import Naked
			Naked()

		if "FootLocker" in answer:
			from modules.FootLocker import FootLocker

			FootLocker()

		if "StreetMachine" in answer:
			from modules.StreetMachine import StreetMachine

			StreetMachine()

		if "ThePlayOffs" in answer:
			from modules.ThePlayOffs import ThePlayOffs

			ThePlayOffs()

		if "Microsoft" in answer:
			from modules.MicrosoftForm import MicrosoftForm

			MicrosoftForm()

		if "Solebox" in answer:
			from modules.Solebox import Solebox

			Solebox()

		if "Courir" in answer:
			from modules.Courir import CourirModule

			CourirModule()

		if "Travis" in answer:
			from modules.TravisScott import TravisScott

			TravisScott()
			
		return self.promptModule()

	def __init__(self):

		printHeader()

		self.runCli()

		print("")
		self.promptModule()

	def runCli(self):
		utilities.setTitle("SyneziaRaffle - 0.1.9.1")

		Instance()

		"""
			UI
		"""

		printHeader()

		"""
			Configuration
		"""

		Configuration()

		"""
			License(s).
		"""

		# Licenser()


if __name__ == "__main__":
	CLI()
