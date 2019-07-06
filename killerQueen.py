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
from diary import *

class SampleAgent(object):

	def __init__(self, agentName):

		self.myname = agentName
		self.sleeptime = 0.1

		self.tracker = Tracker()
		self.diary	 = Diary()

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
		self.diary.nextDay()

		return None

	def talk(self):




		return cb.skip()

	def whisper(self):

		targetId = int(heatSort(self.tracker, heatAttack))
		previousId = self.diary.readTodayNote(label = "attack target")

		if previousId is None:
			#Log choosen target
			self.diary.todayNote("attack target", targetId)
			return cb.attack(targetId)
		else:
			#Check if current target and previous have similar heat
			#Change target if current is higher (in same heatmap)
			heats = heatMap(self.tracker, heatAttack)
			currentHeat = getHeat(targetId, heats)
			previousHeat = getHeat(previousId, heats)

			if currentHeat > previousHeat:
				#Change target
				self.diary.todayNote("attack target", targetId)
				return cb.attack(targetId)
			else :
				return cb.skip()


	def vote(self):

		target = heatSort(self.tracker, heatVote)
		self.diary.todayNote("voted", target)
		return target

	def attack(self):

		target = heatSort(self.tracker, heatAttack)
		self.diary.todayNote("attacked", target)
		return target

	def divine(self):

		target = heatSort(self.tracker, heatDivine)
		self.diary.todayNote("divined", target)
		return target

	def guard(self):

		target = heatSort(self.tracker, heatGuard)
		self.diary.todayNote("guarded", target)
		return target

	def finish(self):

		#log(self.tracker.profiles, json = 1)
		self.tracker.printProfiles()
		#print(getTimeStamp()+" inside Finish")

		print(json.dumps(self.diary.notes))

		return None








if __name__ == '__main__':
	parseArgs(sys.argv[1:])
	aiwolfpy.connect_parse(SampleAgent("FoxuFoxu"))
