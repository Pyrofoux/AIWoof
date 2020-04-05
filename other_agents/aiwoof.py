#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division

# Sample random python-based agent for AIWolf
# Based on https://github.com/k-harada/AIWolfPy
# Developed for aiwolf 0.4.12 (2018/06/16)
# Author: ehauckdo

import aiwolfpy
import aiwolfpy.contentbuilder as cb

#printing of nested dicts and pandas
import json
from tabulate import tabulate

import time
import random
import optparse
import sys

from utility import *

class SampleAgent(object):

	def __init__(self, agent_name):
		self.myname = agent_name
		self.sleeptime = 0.1

	def getName(self):
		return self.myname

	def initialize(self, base_info, diff_data, game_setting):
		self.base_info = base_info
		self.game_setting = game_setting
		printGameSetting(game_setting)

	def update(self, base_info, diff_data, request):
		self.base_info = base_info
		print(getTimeStamp()+" inside Update")
		printBaseInfo(base_info)
		printDiffData(diff_data)

	def dayStart(self):
		print(getTimeStamp()+" inside dayStart")
		return None

	def talk(self):
		print(getTimeStamp()+" inside Talk")
		selected = randomPlayerId(self.base_info)
		print("Selected ID for talk: "+str(selected))
		return cb.vote(selected)

	def whisper(self):
		print(getTimeStamp()+" inside Whisper")
		selected = randomPlayerId(self.base_info)
		print("Selected ID for whisper: "+str(selected))
		return cb.attack(selected)

	def vote(self):
		print(getTimeStamp()+" inside Vote")
		selected = randomPlayerId(self.base_info)
		print("Selected ID for vote: "+str(selected))
		return selected

	def attack(self):
		print(getTimeStamp()+" inside Attack")
		selected = randomPlayerId(self.base_info)
		print("Selected ID for attack: "+str(selected))
		return selected
		
	def divine(self):
		print(getTimeStamp()+" inside Divine")
		selected = randomPlayerId(self.base_info)
		print("Selected ID for divine: "+str(selected))
		return selected

	def guard(self):
		print(getTimeStamp()+" inside Guard")
		selected = randomPlayerId(self.base_info)
		print("Selected ID for guard: "+str(selected))
		return selected
	
	def finish(self):
		print(getTimeStamp()+" inside Finish")
		return None

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

if __name__ == '__main__':	
	parseArgs(sys.argv[1:])
	aiwolfpy.connect_parse(SampleAgent("AIWoof"))
