#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division


import aiwolfpy
import aiwolfpy.contentbuilder as cb

##printing of nested dicts and pandas
import json
from tabulate import tabulate

import time
import random
import optparse
import sys

from toolbox import *
from profileManager import *

class SampleAgent(object):

	def __init__(self, agent_name):
		self.myname = agent_name
		self.sleeptime = 0.1

		clearLog()

	def getName(self):
		return self.myname

	def initialize(self, base_info, diff_data, game_setting):
		self.base_info = base_info
		self.game_setting = game_setting

		log(game_setting)
		log(base_info)

		createProfiles(base_info, game_setting)



	def update(self, base_info, diff_data, request):
		self.base_info = base_info
		#print(getTimeStamp()+" inside Update")
		#printBaseInfo(base_info)

		for index, row in diff_data.iterrows():
			log(row)


	def dayStart(self):



		#print(" inside dayStart")
		return None

	def talk(self):
		#print(getTimeStamp()+" inside Talk")
		selected = randomAliveId(self.base_info)
		#print("Selected ID for talk: "+str(selected))
		return cb.vote(selected)

	def whisper(self):
		#print(getTimeStamp()+" inside Whisper")
		selected = randomAliveId(self.base_info)
		#print("Selected ID for whisper: "+str(selected))
		return cb.attack(selected)

	def vote(self):
		#print(getTimeStamp()+" inside Vote")
		selected = randomAliveId(self.base_info)
		#print("Selected ID for vote: "+str(selected))
		return selected

	def attack(self):
		#print(getTimeStamp()+" inside Attack")
		selected = randomAliveId(self.base_info)
		#print("Selected ID for attack: "+str(selected))
		return selected

	def divine(self):
		#print(getTimeStamp()+" inside Divine")

		selected = randomAliveId(self.base_info)
		#print("Selected ID for divine: "+str(selected))
		return selected

	def guard(self):
		#print(getTimeStamp()+" inside Guard")
		selected = randomAliveId(self.base_info)
		#print("Selected ID for guard: "+str(selected))
		return selected

	def finish(self):



		#print(getTimeStamp()+" inside Finish")
		return None








if __name__ == '__main__':
	parseArgs(sys.argv[1:])
	aiwolfpy.connect_parse(SampleAgent("Killer Q."))
