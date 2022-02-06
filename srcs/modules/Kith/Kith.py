

'''

[Naked] Naked.py

Author: seith <seith.corp@gmail.com>

Created: 27/04/2021 02:47:39 by seith
Updated: 27/04/2021 02:47:39 by seith

Synezia Corp. (c) 2021 - MIT

'''

import PyInquirer

from singleton import Instance

from .account import KithAccountCreator

def get_choices():
	modules = ["Account Creator", PyInquirer.Separator(), "Return"]
	return (modules)

class Kith():

	def __promptModule(self):
		questions = [
			{
				'type': 'list',
				'name': 'choice',
				'message': 'Select a module to Run',
				'choices': get_choices()	
			}
		]

		answer = PyInquirer.prompt(
			questions=questions,
			keyboard_interrupt_msg=f"Cancelled by User. Exiting CLI",
		).get("choice")

		if not answer:
			exit(0)

		if ("Account" in answer):
			KithAccountCreator()

	def __init__(self):

		self.__promptModule()