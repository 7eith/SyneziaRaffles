'''

[Naked] Naked.py

Author: seith <seith.corp@gmail.com>

Created: 27/04/2021 02:47:39 by seith
Updated: 27/04/2021 02:47:39 by seith

Synezia Corp. (c) 2021 - MIT

'''

import PyInquirer
from singleton import Instance
from .raffle import NakedRaffle

def get_choices():
	modules = ["Enter Raffle", PyInquirer.Separator(), "Return"]
	return (modules)

class Naked():

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

		if ("Raffle" in answer):
			NakedRaffle()

	def __init__(self):

		self.__promptModule()