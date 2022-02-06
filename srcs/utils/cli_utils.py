"""

[utils] cli_utils.py

Author: seith <seith.corp@gmail.com>

Created: 27/01/2021 21:19:24 by seith
Updated: 27/01/2021 21:19:24 by seith

Synezia Corp. (c) 2021 - MIT

"""

import os
from pyfiglet import Figlet


def printHeader():
    os.system('cls' if os.name=='nt' else 'clear')
    f = Figlet(font="slant", justify="center")
    print("\033[1;35m")
    print(f.renderText("SyneziaRaffle"))
    print("\t\t\t  \033[94m* Version: Beta - 0.1.9.1")
    print("\033[0m")

def printLine():
    print("==================================================================\n")
