'''

[singleton] controller.py

Author: seith <seith.corp@gmail.com>

Created: 05/03/2021 17:56:24 by seith
Updated: 05/03/2021 17:56:24 by seith

Synezia Corp. (c) 2021 - MIT

'''
import time
import os

import utilities

from .global_singleton import GlobalSingleton
from pypresence import Presence

from logger.logger import Logger

from datetime import datetime

class Instance(metaclass=GlobalSingleton):

	"""
		Constructor
	"""

	def __init__(self):
		self.RPC = None
		self.version = '0.1.9.1'
		self.debug = True

		self.profile = None
		self.role = "Unknown"

		"""
			Date / Time
		"""

		now = datetime.now()
		self.date = '{:02d}_{:02d}_{:02d}-{:02d}-{:02d}'.format(now.day, now.month, now.hour, now.minute, now.second)

		"""
			DiscordRPC
		"""

		if (not self.RPC):
			self.RPC = Presence('807021875242729525') 

			try:
				self.RPC.connect()
			except Exception as error:
				self.RPC = None
				Logger.error('Failed to init DiscordRPC. Launch Discord for Presence if you want')

			if (self.RPC):
				self.RPC.update(
					details="Selecting Raffle...",
					state=self.version, 
					large_image="logo",
					large_text="SyneziaRaffle",
				)

	def initProfile(self, profile):
		del profile["message"]

		self.profile = profile
		self.role = "BETA"
		Logger.info(f"* Welcome [BETA] {profile['tag']}")
		utilities.setTitle(f"SyneziaRaffle [{self.version}] - {profile['tag']}")

	def getProfile(self):
		return (self.profile)
	"""
		getVersion()
			return version.
	"""

	def getVersion(self):
		return (self.version)

	"""
		getDate()
			return Date
	"""
	
	def getDate(self):
		return (self.date)

	"""
		updateRPC(details="Destroying FootLocker)
			update DiscordRPC
	"""

	def updateRPC(self, details='Destroying FootLocker'):
		if (self.RPC):
			self.RPC.update(
				details=details,
				state=self.version, 
				large_image="logo",
				large_text="SyneziaRaffle",
			)