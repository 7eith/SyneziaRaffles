'''

[profiles] profile.py

Author: seith <seith.corp@gmail.com>

Created: 16/03/2021 19:44:03 by seith
Updated: 16/03/2021 19:44:03 by seith

Synezia Corp. (c) 2021 - MIT

'''

import os
import PyInquirer
import glob
import csv

from utils.colors import Color
from logger.logger import Logger

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


class Profile():

	def __init__(self, moduleName):
		self.moduleName = moduleName

	def fetchProfiles(self):
		dir_path = os.getcwd()
		profileFile = self.__getProfileFiles()
		# print(profileFile)
		Logger.info(f"Reading profiles from {profileFile} ...")

		profiles = list(read_csv(dir_path + "/" + profileFile))

		Logger.info(f"{len(profiles)} profiles successfully fetched from {profileFile} !")
		self.profileFile = profileFile
		
		return list(profiles)

	""" 
		getProfile Files
			return File
	"""

	def __getProfileFiles(self):
		if len(glob.glob(f"profiles/{self.moduleName}/*.csv")) < 1:
			Logger.error('No profiles found in directory.')
			Logger.info(f"Put profiles in profiles/{self.moduleName}/ it's updating in live")

			try:
				input("[{}] Press Enter for retrying or exit CLI.".format(Logger.getTime()))
			except KeyboardInterrupt:
				return exit(0)
				
			return self.__getProfileFiles()

		questions = [
			{
				'type': 'list',
				'name': 'choice',
				'message': 'Select a profiles file.',
				'choices': glob.glob(f"profiles/{self.moduleName}/*.csv")
			}
		]

		answer = (
			PyInquirer.prompt(questions=questions, keyboard_interrupt_msg=f"{Color.RED}Cancelled by User. Exiting CLI{Color.RESET}")
			.get("choice")
		)

		if not answer:
			exit(0)

		return answer.strip()