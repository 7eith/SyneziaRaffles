import requests
import PyInquirer
from datetime import datetime

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

from logger.logger import Logger

class SizeValidator(PyInquirer.Validator):
	def validate(self, document):
		values = document.text.split(",")
		
		if (len(values) != 2):
			raise PyInquirer.ValidationError(
				message='Enter a delay in seconds like : 5, 45 (Must be an Number separated by comma)',
				cursor_position=len(document.text))  # Move cursor to end

		try:
			min = int(values[0])
			max = int(values[1])
		except ValueError:
			raise PyInquirer.ValidationError(
				message='Enter a delay in seconds like : 5, 45 (Must be an Number separated by comma)',
				cursor_position=len(document.text))  # Move cursor to end


def fetchLivesRaffle(hasEnded=False):
	headers = {
		'Host': 'eql.xyz',
		'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
		'origin': 'https://eql.xyz',
		'sec-ch-ua-mobile': '?0',
		'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
		'accept': 'application/signed-exchange;v=b3;q=0.9,*/*;q=0.8',
		'purpose': 'prefetch',
		'sec-fetch-site': 'same-origin',
		'sec-fetch-mode': 'cors',
		'sec-fetch-dest': 'empty',
		'referer': 'https://eql.xyz/en-GB/launch/courir/nike-dunk-high-game-royal/',
		'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7',
		'dnt': '1',
		'pragma': 'no-cache',
		'cache-control': 'no-cache',
	}

	try:
		response = requests.get('https://eql.xyz/page-data/en-GB/launch/courir/page-data.json', headers=headers)

		items = response.json()["result"]["data"]["allPrismicDraw"]["nodes"]
	except Exception as error:
		Logger.error(error)
		Logger.error("Failed to fetch live raffles... Retrying ")

	return (items)

def fetchSizesFromSlug(slug):
	headers = {
		'Host': 'eql.xyz',
		'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
		'origin': 'https://eql.xyz',
		'sec-ch-ua-mobile': '?0',
		'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
		'accept': 'application/signed-exchange;v=b3;q=0.9,*/*;q=0.8',
		'purpose': 'prefetch',
		'sec-fetch-site': 'same-origin',
		'sec-fetch-mode': 'cors',
		'sec-fetch-dest': 'empty',
		'referer': 'https://eql.xyz/en-GB/launch/courir/{}/'.format("slug"),
		'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7',
		'dnt': '1',
		'pragma': 'no-cache',
		'cache-control': 'no-cache',
	}

	try:
		response = requests.get('https://eql.xyz/page-data/en-GB/launch/courir/{}/page-data.json'.format(slug), headers=headers)
		item = response.json()["result"]["data"]["prismicDraw"]["data"]

		sizes = list()
		for size in item["inventory"]:
			sizes.append(size['variant_title'])
		
		return (sizes)

	except Exception as error:
		Logger.error(error)
		Logger.error("Failed to fetch sizes... Retrying ")

def promptCourirRaffle():
	raffles = fetchLivesRaffle()

	rafflesListed = list()
	now = datetime.now().timestamp()

	activeRaffles = [raffle for raffle in raffles if now > parse(raffle['data']['start']).timestamp() and now < parse(raffle['data']['end']).timestamp()]
	soonRaffles = [raffle for raffle in raffles if now < parse(raffle['data']['start']).timestamp()]
	endedRaffle = [raffle for raffle in raffles if now > parse(raffle['data']['end']).timestamp()]

	for raffle in activeRaffles:
		payload = {
			"name": raffle["data"]["product"],
			"value": raffle["data"]
		}

		rafflesListed.append(payload)
	
	rafflesListed.append(PyInquirer.Separator("------- Soon -------"))
	for raffle in soonRaffles:
		payload = {
			"name": raffle["data"]["product"],
			"disabled": f"Start: {raffle['data']['start']}"
		}

		rafflesListed.append(payload)
	 
	questions = [
		{
			'type': 'list',
			'name': 'choice',
			'message': 'Select Raffle...',
			'choices': rafflesListed
		}
	]

	answer = PyInquirer.prompt(
		questions=questions,
		keyboard_interrupt_msg=f"Cancelled by User. Exiting CLI",
	).get("choice")

	if not answer:
		exit(0)
	
	return (answer)


def promptSizeRanges(sizes):
	questions = [
		{
			'type': 'input',
			'name': 'size',
			'message': 'Enter Size Ranges separated by Comma (like 0, 100 for full size range)',
			'default': '0, 100',
			'validate': SizeValidator
		},
	]

	answer = (
		PyInquirer.prompt(questions=questions, keyboard_interrupt_msg=f"Cancelled by User. Exiting CLI")
		.get("size")
	)

	delayAnswer = answer.split(",")

	minSize = int(delayAnswer[0])
	maxSize = int(delayAnswer[1])

	validatedSizes = [size for size in sizes if int(size.split(' ')[1]) > minSize and int(size.split(' ')[1]) < maxSize]

	if not validatedSizes:
		Logger.error("Invalid Size Range or Empty Size Range check your size Range!")
		return promptSizeRanges(sizes)
	return (validatedSizes)