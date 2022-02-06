"""

[initer] initer.py

Author: seith <seith.corp@gmail.com>

Created: 09/03/2021 19:45:39 by seith
Updated: 09/03/2021 19:45:39 by seith

Synezia Corp. (c) 2021 - MIT

"""

import os
from logger.logger import Logger


class Initer:
	def __init__(self):
		Logger.info(
			"Welcome! I see its your first run? Read carrefully guides before do anything."
		)

	def firstRun(self):
		"""
		Create default Directory needed by CLI
		"""
		dirs = ["profiles", "logs", "outputs", "inputs", "proxies"]

		for directory in dirs:
			try:
				os.mkdir(directory)
			except FileExistsError:
				pass

		"""
			Create profiles directory
		"""

		# Modules Directory
		moduleDirs = [
			"TheBrokenArm",
			"FootLocker",
			"FootPatrol",
			"Tools",
			"StreetMachine",
			"ThePlayOffs",
			"MicrosoftForm",
			"Solebox",
			"Naked",
			"Kith",
			"GoogleForm",
			"Impact",
			"Citadium"
		]

		for directory in moduleDirs:
			try:
				os.mkdir(f"profiles/{directory}")
				os.mkdir(f"logs/{directory}")
				os.mkdir(f"proxies/{directory}")
			except FileExistsError:
				pass

		f = open("profiles/FootLocker/profiles_example.csv", "w")
		f.write(f"first_name,last_name,email,password,country\n")
		f.write(
			f"Abdou,Des Halles,abdoudeshalles@synezia.com,AbdouDonneMaPaire93100,fr\n"
		)
		f.close()

		f = open("profiles/StreetMachine/profiles_example.csv", "w")
		f.write(f"first_name,last_name,email,password\n")
		f.write(f"Abdou,Des Halles,abdoudeshalles@synezia.com,AbdouDonneMaPaire93100\n")
		f.close()

		f = open("profiles/ThePlayOffs/profiles_example.csv", "w")
		f.write(
			f"first_name,last_name,email,instagram,size,payment,country,city,address,zipCode,phone\n"
		)
		f.write(
			f"Abdou,Des Halles,abdoudeshalles@synezia.com,FootLockerEU,2,France,Paris,42 rue rivoli,75015,+33645171275\n"
		)
		f.close()

		f = open("profiles/Solebox/profiles_example.csv", "w")
		f.write(
			f"email,first_name,last_name,instagram,phone,month,day,shop,size,country,gender\n"
		)
		f.write(
			f"seith@synezia.com,Keyzer,Soze,keyzer.soze,+33666 or 666,09,11,Brussels,US7 / EU40,Iris,France,Male\n"
		)
		f.close()

		f = open("profiles/Kith/profiles_example.csv", "w")
		f.write(
			f"email,password,first_name,last_name,address,country,city,zipCode,phone\n"
		)
		f.write(
			f"seith@synezia.com,SyneziaToTheMoon,Neal,Caffrey,42 rue de rivoli,France,Paris,93270,0666\n"
		)
		f.close()

		f = open("profiles/Naked/profiles_example.csv", "w")
		f.write(
			f"email,first_name,last_name,address,countryCode,city,zipCode,phone,instagram\n"
		)
		f.write(
			f"seith@synezia.com,Pablo,EscrocDBar,42 rue de rivoli,FR,Paris,75000,0666,seithh_\n"
		)
		f.close()

		f = open("profiles/Citadium/profiles_example.csv", "w")
		f.write(
			f"firstname,lastname,phone,departement,size\n"
		)
		f.write(
			f"Omar,Little,0666661775,75,44\n"
		)
		f.close()

		f = open("profiles/Impact/profiles_example.csv", "w")
		f.write(
			f"firstname,lastname,email,addy,zip,city,phone,country,size\n"
		)
		f.write(
			f"Omar,Little,ehyoomariscoming@synezia.com,42 rue de Rivoli,75018,Paris,0666661775,France,41 1/3 EU - 8 US\n"
		)
		f.close()

		f = open("profiles/TheBrokenArm/profiles_example.csv", "w")
		f.write(
			f"firstname,lastname,email,phone,size,days,months,years\n"
		)
		f.write(
			f"Omar,Little,thewiregoat@gmail.com,06666,9 US,25,10,2015\n"
		)
		f.close()