import aiwolfpy
import aiwolfpy.contentbuilder as cb

import sys
from toolbox import *
from tracker import *
from heatSort import *
from diary import *

import roleBehaviors

class Base(object):

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

		#Initialise profiles for each player
		self.tracker.createProfiles(baseInfo, gameSetting)
		self.tracker.update(baseInfo, diffData, self.diary)

		#Load behavior functions
		self.assignRole(self.tracker.myRole)


	def update(self, baseInfo, diffData, request):
		self.baseInfo = baseInfo
		self.tracker.update(baseInfo, diffData, self.diary)

	def dayStart(self):

		self.tracker.nextDay()
		self.diary.nextDay()

		self.talkCount = 0
		self.whisperCount = 0

		return None

	def talk(self):

		self.talkCount += 1

		return cb.skip()


	def vote(self):

		target = heatSort(self.tracker, heatVote)
		self.diary.todayNote("voted", target)
		return target


	def finish(self):

		self.tracker.logProfiles()
		self.diary.logNotes()

		return None

	def assignRole(self, roleName):

		# Change the current's object Class to match the corresponding role
		self.__class__ = eval("roleBehaviors."+roleName)
