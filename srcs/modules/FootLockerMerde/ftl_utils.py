"""

[FootLocker] ftl_utils.py

Author: seith <seith.corp@gmail.com>

Created: 27/01/2021 23:32:55 by seith
Updated: 27/01/2021 23:32:55 by seith

Synezia Corp. (c) 2021 - MIT

"""

import requests
import inquirer
import random
from proxy.controller import ProxyManager
import datetime

def initSession(proxy=None, accessToken=None, sessionId=None):

    session = requests.Session()

    if proxy is None:
        proxy = ProxyManager().getProxy()

    if accessToken is None or sessionId is None:
        headers = {
            "Host": "www.footlocker.eu",
            "x-flapi-timeout": "42894",
            "x-flapi-session-id": "d4496b1ad80efde3c156dfc99.apigeeHostInstance",
            "x-fl-app-version": "4.6.4",
            "x-flapi-api-identifier": "921B2b33cAfba5WWcb0bc32d5ix89c6b0f614",
            "x-fl-device-id": "68DDAFA4-5645-4525-A1B5-DD0FE0D96417",
            "accept": "application/json",
            "accept-language": "fr-FR,fr;q=0.8",
            "x-api-key": "DjpcK97IzdUPQGvv9rX8FEcINrbqzZRt",
            "user-agent": "FLEU/CFNetwork/Darwin",
            "x-api-country": "FR",
            "x-api-lang": "fr-FR",
            "x-fl-request-id": "BEC36DA9-275F-472A-93A4-74111F78775F",
            "pragma": "no-cache",
            "cache-control": "no-cache",
        }
    else:
        headers = {
            "user-agent": "FLEU/CFNetwork/Darwin",
            "x-flapi-resource-identifier": accessToken,
            "x-flapi-session-id": sessionId,
        }

    response = requests.get(
        "https://www.footlocker.eu/api/session", headers=headers, proxies=proxy
    )

    if response.status_code == 403:
        print(response.text)
        print("[Error] Session Proxy Banned!")
        return initSession()

    if "url" in response.json():
        print("[Error] Captcha!")
        return initSession()

    sessionID = response.headers.get("x-flapi-session-id")
    csrfToken = response.json()["data"]["csrfToken"]

    return {"sessionId": sessionID, "csrfToken": csrfToken, "session": session}


def fetchActiveReleases(sessionData=None):
    proxy = ProxyManager().getProxy()

    if sessionData is None:
        sessionData = initSession(proxy)

    headers = {
        "Host": "www.footlocker.eu",
        "x-time-zone": "Europe/Paris",
        "x-flapi-timeout": "42854",
        "x-fl-app-version": "4.6.4",
        "x-flapi-api-identifier": "921B2b33cAfba5WWcb0bc32d5ix89c6b0f614",
        "x-flapi-session-id": sessionData["sessionId"],
        "x-fl-device-id": "68DDAFA4-5645-4525-A1B5-DD0FE0D96417",
        "accept": "application/json",
        "accept-language": "fr-FR,fr;q=0.8",
        "x-api-key": "DjpcK97IzdUPQGvv9rX8FEcINrbqzZRt",
        "user-agent": "FLEU/CFNetwork/Darwin",
        "x-api-country": "FR",
        "x-api-lang": "fr-FR",
        "x-fl-request-id": "BFEEF1D8-46FE-4AB3-806C-7C2834DC2B13",
        "pragma": "no-cache",
        "cache-control": "no-cache",
    }

    response = sessionData["session"].get(
        "https://www.footlocker.eu/api/release-calendar", proxies=proxy
    )

    if response.status_code == 403:
        print("Fetch active Releases - Proxy banned... Switching proxy.")
        ProxyManager().banProxy(proxy["https"])
        return fetchActiveReleases(sessionData)

    releases = response.json()["releaseCalendarProducts"]
    releaseReservation = [x for x in releases if "reservation" in x]
    activeReleases = [
        x for x in releaseReservation if x["reservation"]["statusCode"] > 0
    ]

    formatedReleases = list()

    for data in activeReleases:
        payload = {
            "pid": data["reservation"]["productId"],
            "name": data["name"],
            "sizes": data["reservation"]["sizes"],
            "price": data["reservation"]["prices"]["fr"],
        }
        formatedReleases.append(payload)

    return formatedReleases


def fetchShops(pid, addy):
    proxy = ProxyManager().getProxy()

    headers = {
        "x-api-key": "DjpcK97IzdUPQGvv9rX8FEcINrbqzZRt",
        "user-agent": "FLEU/CFNetwork/Darwin",
    }

    params = {"procedure": "2", "sku": pid, "address": addy}

    response = requests.get(
        "https://www.footlocker.eu/api/launch-stores",
        headers=headers,
        params=params,
        proxies=proxy,
    )
    stores = response.json()["stores"]

    formatedStores = list()

    for store in stores:
        payload = {
            "id": store["id"],
            "name": store["displayName"],
            "addy": store["address"]["formattedAddress"],
        }
        formatedStores.append(payload)

    return formatedStores


def promptSizes(sizes):
    questions = [
        inquirer.Text(
            "size",
            message="What size do you want to enter? (min 0, max 100, separate by swoosh, in EU size)",
            default="0, 100",
        )
    ]

    answer = inquirer.prompt(questions).get("size").strip()
    sizeAnswer = answer.split(",")

    if len(sizeAnswer) != 2:
        print("Error, please use: LOWEST SIZE IN NUMBER, MAX SIZE IN NUMBER")
        return promptSizes(sizes)

    min = float(sizeAnswer[0])
    max = float(sizeAnswer[1])

    sizes = [x for x in sizes if float(x["eu"]) >= min and float(x["eu"]) <= max]
    return sizes

def get_random_date():

	# try to get a date
	try:
		date = datetime.datetime.strptime('{} {}'.format(random.randint(1, 366), random.randint(1990, 2003)), '%j %Y')
		dateSplit = str(date).split(' ')[0]

		parsed = dateSplit.split('-')
		text = parsed[1] + '/' + parsed[2] + '/' + parsed[0]

		return text
	# if the value happens to be in the leap year range, try again
	except ValueError:
		get_random_date()