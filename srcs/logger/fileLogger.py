"""

[logger] fileLogger.py

Author: seith <seith.corp@gmail.com>

Created: 08/02/2021 21:48:49 by seith
Updated: 08/02/2021 21:48:49 by seith

Synezia Corp. (c) 2021 - MIT

"""

def createFileLogger(fileName, headers):

	textHeaders = ",".join(headers)
	_f = open(fileName, "w")
	_f.write(f"state,{textHeaders}\n")
	_f.close()