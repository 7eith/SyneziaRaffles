'''

[confirmer] utils.py

Author: seith <seith.corp@gmail.com>

Created: 13/04/2021 02:09:23 by seith
Updated: 13/04/2021 02:09:23 by seith

Synezia Corp. (c) 2021 - MIT

'''

from logger.logger import Logger

import PyInquirer
import glob
import os

import requests
import re
import urllib.parse

from utils.colors import Color

def readLinks():
	""" Select File """
	if len(glob.glob(f"inputs/*")) < 1:
		Logger.error('No files found in directory.')
		Logger.info(f"Put links in inputs. When it's done press Enter.")

		try:
			input("[{}] Press Enter for retrying or exit CLI.".format(Logger.getTime()))
		except KeyboardInterrupt:
			return exit(0)
			
		return self.__selectProxiesFile()

	questions = [
		{
			'type': 'list',
			'name': 'choice',
			'message': 'Select a links file',
			'choices': glob.glob(f"inputs/*")
		}
	]

	answer = (
		PyInquirer.prompt(questions=questions, keyboard_interrupt_msg=f"{Color.RED}Cancelled by User. Exiting CLI{Color.RESET}")
		.get("choice")
	)

	if not answer:
		exit(0)

	""" Read File """

	file = answer.strip()

	Logger.info(f"Reading links from {file} ...")
	
	_f = open(file, "r", encoding="utf-8", newline="")

	links = []
	lines = _f.readlines()
	for line in lines:
		links.append(line.strip())

	_f.close()

	Logger.success(f"Readed {len(links)} links from {file} ...")

	return (links)

def flx_GetActivationLink(link):
	res = requests.get(link)

	matcher = re.search("URL='(.+?)'", res.text)
	activationLink = matcher.group(1)

	return (activationLink)

def ExtractActivationTokenFromLink(link):
	parsedQS = urllib.parse.parse_qsl(link.split('?')[1])
	activationToken = parsedQS[0][1]

	return (activationToken)