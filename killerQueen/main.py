#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division

##printing of nested dicts and pandas
import json
from tabulate import tabulate

import time
import random
import optparse
import sys
import argparse

from toolbox import *
from roleBehaviors import *

playerName = "FoxuFoxu"


class KillerQueen(Base):
	pass

if __name__ == '__main__':

	killerQueen = KillerQueen(playerName)

	parseArgs(sys.argv[1:])
	aiwolfpy.connect_parse(killerQueen)
