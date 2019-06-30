#printing of nested dicts and pandas
import json as JSON
import time
import random
import logging
import os


import optparse
from string import digits

from tabulate import tabulate

def printBaseInfo(base_info):
	print("Base Info:")
	print(JSON.dumps(base_info, indent=4))

def printGameSetting(game_setting):
	print("Game Setting:")
	print(JSON.dumps(game_setting, indent=4))

def printDiffData(diff_data):
	print("Diff Data:")

	#No tabulate library on the game server
	#print(tabulate(diff_data, headers='keys', tablefmt='plain'))
	print(diff_data.to_string())

def getTimeStamp():
	return time.strftime('%l:%M:%S%p')

def randomAliveId(base_info):
	ids = getAliveId(base_info)
	return random.choice(ids)

def getAliveId(base_info):
	ids = []
	for key,value in base_info["statusMap"].items():
		if value == "ALIVE" and int(key) != base_info["agentIdx"]:
			ids.append(int(key))
	return ids

def formatDivine(text):

	chunked = text.split()
	info = {}
	info['team'] = chunked[2]
	info['id'] = formatAgentId(chunked[1])
	return info

def formatAgentId(txt):
	return str(int(''.join(c for c in txt if c in digits)))



logFileName = "../log.last"
def clearLog():
	if os.path.exists(logFileName):
  		os.remove(logFileName)

def log(input="", json = False):
	f = open(logFileName,"a+")

	if json :
		output = JSON.dumps(input, indent=4)
	else :
		output = str(input)

	f.write(output)
	f.write('\n')




def parseArgs(args):
	usage = "usage: %prog [options]"
	parser = optparse.OptionParser(usage=usage)

	# need this to ensure -h can be used as an option
	parser.set_conflict_handler("resolve")

	parser.add_option('-h', action="store", type="string", dest="hostname",
		help="IP address of the AIWolf server", default=None)
	parser.add_option('-p', action="store", type="int", dest="port",
		help="Port to connect in the server", default=None)
	parser.add_option('-r', action="store", type="string", dest="port",
		help="Role request to the server", default=-1)

	(opt, args) = parser.parse_args()
	if opt.hostname == None or opt.port == -1:
		parser.print_help()
		sys.exit()
