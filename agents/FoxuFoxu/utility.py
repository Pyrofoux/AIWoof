#printing of nested dicts and pandas
import json
import time
import random
from tabulate import tabulate

def printBaseInfo(base_info):
	print("Base Info:")
	print(json.dumps(base_info, indent=4))

def printGameSetting(game_setting):
	print("Game Setting:")
	print(json.dumps(game_setting, indent=4))

def printDiffData(diff_data):
	print("Diff Data:")

	#No tabulate library on the game server
	#print(tabulate(diff_data, headers='keys', tablefmt='plain'))
	print(diff_data.to_string())

def getTimeStamp():
	return time.strftime('%l:%M:%S%p')

def randomPlayerId(base_info):
	ids = getAlivePlayerIds(base_info)
	return random.choice(ids)

def getAlivePlayerIds(base_info):
	ids = []
	for key,value in base_info["statusMap"].items():
		if value == "ALIVE" and int(key) != base_info["agentIdx"]:
			ids.append(int(key))
	return ids
