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

	def __init__(self, agentName):
		self.myname = agentName
		self.sleeptime = 0.1

		clearLog()

	def getName(self):
		return self.myname

	def initialize(self, baseInfo, diffData, gameSetting):
		self.baseInfo = baseInfo
		self.gameSetting = gameSetting

		log(gameSetting)
		log(baseInfo)

		createProfiles(baseInfo, gameSetting)



	def update(self, baseInfo, diffData, request):
		self.baseInfo = baseInfo
		#print(getTimeStamp()+" inside Update")
		#printBaseInfo(baseInfo)

		for index, row in diffData.iterrows():
			log(row)


	def dayStart(self):



		#print(" inside dayStart")
		return None

	def talk(self):
		#print(getTimeStamp()+" inside Talk")
		selected = randomAliveId(self.baseInfo)
		#print("Selected ID for talk: "+str(selected))
		return cb.vote(selected)

	def whisper(self):
		#print(getTimeStamp()+" inside Whisper")
		selected = randomAliveId(self.baseInfo)
		#print("Selected ID for whisper: "+str(selected))
		return cb.attack(selected)

	def vote(self):
		#print(getTimeStamp()+" inside Vote")
		selected = randomAliveId(self.baseInfo)
		#print("Selected ID for vote: "+str(selected))
		return selected

	def attack(self):
		#print(getTimeStamp()+" inside Attack")
		selected = randomAliveId(self.baseInfo)
		#print("Selected ID for attack: "+str(selected))
		return selected

	def divine(self):
		#print(getTimeStamp()+" inside Divine")

		selected = randomAliveId(self.baseInfo)
		#print("Selected ID for divine: "+str(selected))
		return selected

	def guard(self):
		#print(getTimeStamp()+" inside Guard")
		selected = randomAliveId(self.baseInfo)
		#print("Selected ID for guard: "+str(selected))
		return selected

	def finish(self):



		#print(getTimeStamp()+" inside Finish")
		return None








if __name__ == '__main__':
	parseArgs(sys.argv[1:])
	aiwolfpy.connect_parse(SampleAgent("Killer Q."))
