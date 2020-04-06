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

		clearLog()

	def getName(self):
		return self.myname

	def initialize(self, baseInfo, diffData, gameSetting):
		self.baseInfo = baseInfo
		self.gameSetting = gameSetting

		log(gameSetting)
		log(baseInfo)

		self.tracker = Tracker()
		self.diary	 = Diary()

		#Keep tracks of how many times we had to talk today
		self.talkCount = 0

		#Keep tracks of how many times we had to talk today
		self.whisperCount = 0


		self.tracker.createProfiles(baseInfo, gameSetting)
		self.tracker.update(baseInfo, diffData, self.diary)
		#log(self.tracker.profiles)


	def update(self, baseInfo, diffData, request):
		self.baseInfo = baseInfo
		self.tracker.update(baseInfo, diffData, self.diary)

	def dayStart(self):

		self.tracker.nextDay()
		self.diary.nextDay()

		self.talkCount = 0
		self.whisperCount = 0


		if self.tracker.myRole == "POSSESSED":
			#POSSESSED disguise as a SEER and does fake divinations

			fakeList = self.diary.readNodayNote("fakeDivinedList")

			if fakeList is None:
				fakeList = [self.tracker.myId]

			alives = getAliveId(self.baseInfo)
			remaining = [id for id in alives if not id in fakeList]

			if len(remaining) > 0:
				target = random.choice(remaining)

				fakeList.append(target)

				self.diary.todayNote("fakeDivined", {'id':target, 'team':'HUMAN'})
				self.diary.nodayNote("fakeDivinedList", fakeList)
		return None

	def talk(self):

		self.talkCount += 1


		#Tell about our divinations if we're SEER
		#Code should be refactored in proper module

		#Todo : don't reveal until we find a werewolf
		#or there's like only 65% of remaining alive

		#Todo : POSSESSED tell about its fake divinations
		#and randomly select someone to fake divine as human every day

		if self.tracker.myRole == "SEER":

			#Reveal all our divinations when we have seen a wolf or when there's 60% alive players
			if (self.tracker.totalAlivePlayers <= 0.60*self.tracker.totalPlayers)  or (self.diary.readNodayNote('seenWolf') == True):
				divinations = self.diary.readAllNotes(label = "divined")

				dayCount = 0
				for day in sorted(divinations.keys(), reverse=True):

					dayCount += 1
					if self.talkCount == dayCount+1:
						divination = divinations[day]['divined']
						id = divination['id']
						team = divination['team']
						return "DAY "+str(day)+" ("+cb.divined(int(id), team)+")"

					elif self.talkCount == 1:
						return cb.comingout(int(self.tracker.myId), "SEER")

		if self.tracker.myRole == "MEDIUM":
			#Reveal all our divinations when we have seen a wolf or when there's 60% alive players
			if (self.tracker.totalAlivePlayers <= 0.60*self.tracker.totalPlayers) or (self.diary.readNodayNote('seenWolf') == True):
			#if  False:
				divinations = self.diary.readAllNotes(label = "identified")

				dayCount = 0
				for day in sorted(divinations.keys(), reverse=True):

					dayCount += 1
					if self.talkCount == dayCount+1:
						divination = divinations[day]['identified']
						id = divination['id']
						team = divination['team']
						return "DAY "+str(day)+" ("+cb.identified(int(id), team)+")"

					elif self.talkCount == 1:
						return cb.comingout(int(self.tracker.myId), "MEDIUM")

		if self.tracker.myRole == "POSSESSED":

			divinations = self.diary.readAllNotes(label = "fakeDivined")

			dayCount = 0
			for day in sorted(divinations.keys(), reverse=True):

				dayCount += 1
				if self.talkCount == dayCount+1:
					divination = divinations[day]['fakeDivined']
					id = divination['id']
					team = divination['team']
					return "DAY "+str(day)+" ("+cb.divined(int(id), team)+")"

				elif self.talkCount == 1:
					return cb.comingout(int(self.tracker.myId), "SEER")

		return cb.skip()

	def whisper(self):
		#Only Wolves can whisper
		self.whisperCount += 1

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
				self.diary.todayNote("changed target")
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
		#Only SEER can divine
		target = heatSort(self.tracker, heatDivine)
		self.diary.todayNote("guarded", target)
		return target

	def guard(self):
		#only BODYGUARD can guard
		target = heatSort(self.tracker, heatGuard)
		self.diary.todayNote("guarded", target)
		return target

	def finish(self):

		self.tracker.logProfiles()
		self.diary.logNotes()

		return None








if __name__ == '__main__':
	parseArgs(sys.argv[1:])
	aiwolfpy.connect_parse(SampleAgent("FoxuFoxu"))
