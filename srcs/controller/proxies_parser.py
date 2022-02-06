"""

[parser] proxies_parser.py

Author: seith <seith.corp@gmail.com>

Created: 28/01/2021 14:28:27 by seith
Updated: 28/01/2021 14:28:27 by seith

Synezia Corp. (c) 2021 - MIT

"""

import glob
import inquirer
import csv
import os


def read_proxies(proxies_file_name):
    _f = open(proxies_file_name, "r", encoding="utf-8", newline="")

    formatedProxies = []
    proxies = _f.readlines()
    for line in proxies:

        line = line.strip()
        line = line.split(":")
        formatedProxies.append(
            "http://" + line[2] + ":" + line[3] + "@" + line[0] + ":" + line[1]
        )

    return formatedProxies


def fetchProxiesFile():
    questions = [
        inquirer.List(
            "choice",
            message="What action do you want to run?",
            choices=glob.glob("inputs/proxies/*"),
        ),
    ]

    answers = inquirer.prompt(questions)

    if answers:
        return answers.get("choice").strip()


def fetchProxies():
    dir_path = os.getcwd()
    proxiesFile = fetchProxiesFile()
    print("[Info] Fetching proxyes...")
    proxies = read_proxies(dir_path + "/" + proxiesFile)
    print("[Info] {} proxies fetched.".format(len(list(proxies))))

    return proxies
