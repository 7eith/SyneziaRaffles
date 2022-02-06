'''

[confirmer] confirmer.py

Author: seith <seith.corp@gmail.com>

Created: 13/04/2021 02:02:25 by seith
Updated: 13/04/2021 02:02:25 by seith

Synezia Corp. (c) 2021 - MIT

'''

import PyInquirer

import utilities

from .nr import FootLockerLinkConfirmer

from logger.logger import Logger
from utils.colors import Color

class FootLockerConfirmer():

	def __init__(self):
		utilities.printHeader()
		
		""" Select Type """
		FootLockerLinkConfirmer()