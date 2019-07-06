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
from tracker import *
from heatSort import *

class SampleAgent(object):

	def __init__(self, agentName):

		self.myname = agentName
		self.sleeptime = 0.1

		self.tracker = Tracker()

		clearLog()

	def getName(self):
		return self.myname

	def initialize(self, baseInfo, diffData, gameSetting):
		self.baseInfo = baseInfo
		self.gameSetting = gameSetting

		log(gameSetting)
		log(baseInfo)

		self.tracker.createProfiles(baseInfo, gameSetting)
		#log(self.tracker.profiles)


	def update(self, baseInfo, diffData, request):
		self.baseInfo = baseInfo
		self.tracker.update(baseInfo, diffData)

	def dayStart(self):

		self.tracker.nextDay()

		return None

	def talk(self):
		return cb.skip()

	def whisper(self):

		targetId = int(heatSort(self.tracker, heatAttack))
		return cb.attack(targetId)

	def vote(self):
		return heatSort(self.tracker, heatVote)

	def attack(self):
		return heatSort(self.tracker, heatAttack)

	def divine(self):
		return heatSort(self.tracker, heatDivine)

	def guard(self):
		return heatSort(self.tracker, heatGuard)

	def finish(self):

		#log(self.tracker.profiles, json = 1)

		#print(getTimeStamp()+" inside Finish")
		return None








if __name__ == '__main__':
	parseArgs(sys.argv[1:])
	aiwolfpy.connect_parse(SampleAgent("FoxuFoxu"))
