"""

[parser] profile_parser.py

Author: seith <seith.corp@gmail.com>

Created: 28/01/2021 14:28:20 by seith
Updated: 28/01/2021 14:28:20 by seith

Synezia Corp. (c) 2021 - MIT

"""

import glob
import inquirer
import csv
import os
import string
import random

from logger.logger import Logger
from utils.cli_utils import printLine, printHeader

def read_csv(csv_file_name, remove_chars=None):

	_f = open(csv_file_name, "r", encoding="utf-8", newline="")

	for _row in csv.DictReader(_f, delimiter=","):

		if remove_chars:

			_cleared_row = {}

			for _k, _v in _row.items():

				for _char in remove_chars:

					_cleared_row[_k.replace(_char, "")] = _v.replace(_char, "")

			yield _cleared_row

		else:

			yield _row

	_f.close()


def fetchProfileFile(moduleName):
	questions = [
		inquirer.List(
			"choice",
			message="Which CSV do you want to use?",
			choices=glob.glob(f"profiles/{moduleName}/*.csv"),
		),
	]

	answers = inquirer.prompt(questions)

	if answers:
		return answers.get("choice").strip()

def generateFakeNumber():
	prefixs = list({ '06', '07' })
	
	numbers = ''.join(random.sample(string.digits, 8))
	
	prefix = random.choice(prefixs)
	number = f"{prefix}{numbers}"
	return (number)

def fetchProfiles(moduleName):
	print("\n")
	printLine()

	dir_path = os.getcwd()
	profileFile = fetchProfileFile(moduleName)

	Logger.info(f"Reading profiles from {profileFile} ...")

	profiles = list(read_csv(dir_path + "/" + profileFile))

	Logger.info(f"{len(profiles)} profiles successfully fetched from {profileFile} !")

	if (moduleName == "TBA"):
		for index, profile in enumerate(profiles):
			# days
			if (profile['days'] == 'RANDOM'):
				profile['days'] = str(random.randint(1, 30))

			if (profile['months'] == 'RANDOM'):
				profile['months'] = str(random.randint(1, 12))

			if (profile['years'] == 'RANDOM'):
				profile['years'] = str(random.randint(1885, 2002))

			if (profile['phone'] == 'RANDOM'):
				profile['phone'] = generateFakeNumber()

	return profiles
