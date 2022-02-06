"""

[FTL] footlocker_module.py

Author: seith <seith.corp@gmail.com>

Created: 10/02/2021 18:16:59 by seith
Updated: 10/02/2021 18:16:59 by seith

Synezia Corp. (c) 2021 - MIT

"""

import requests
import json
import inquirer
import glob
import random

from .account.account_module import FootLockerAccountCreaterModule
from .raffle.raffle_module import FootLockerRaffleModule
from .check.ftl_checker_module import FootLockerCheckerModule

class FootLockerNewRegion:

	def __init__(self):
		self.version = '1.0.0'

		FootLockerAccountCreaterModule()