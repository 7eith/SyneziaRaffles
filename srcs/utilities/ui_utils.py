'''

[utilities] ui_utils.py

Author: seith <seith.corp@gmail.com>

Created: 03/04/2021 17:36:09 by seith
Updated: 03/04/2021 17:36:09 by seith

Synezia Corp. (c) 2021 - MIT

'''

import os
from pyfiglet import Figlet

"""
	setTitle(title)
		set title to Console
"""

def setTitle(title):
	if (os.name == "nt"):
		os.system("title " + title)
	else:
		print(f"\33]0;{title}\a", end='', flush=True)

"""
	clearConsole()
		clear Console
"""

def clearConsole():
	if (os.name == "nt"):
		os.system("cls")
	else:
		os.system("clear")

def printLine():
    print("========================================================================\n")

def printHeader():
    clearConsole()
    f = Figlet(font="slant", justify="center")
    print("\033[1;35m")
    print(f.renderText("SyneziaRaffle"))
    print("\t\t\t  \033[94m* Version: Beta - 0.1.9.1")
    print("\033[0m")
