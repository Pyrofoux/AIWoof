from __future__ import division
from toolbox import *

# Functions to keep track of informations of what we did during the
# previous days, and planning for next actions


class Diary(object):

    def __init__(self):
        self.today = 0
        self.notes = {}

    def nextDay(self):
        self.today += 1

    def writeNote(self, day, label, value):
        #Creates a note for given day, with specific label
        day = int(day)

        if not (day in self.notes):
            self.notes[day] = {}

        self.notes[day][label] = value

    def todayNote(self, label, value):
        #Creates note at current day
        self.writeNote(self.today, label, value)


    def readAllNotes(self, label=False, day=False):
        #Return saved notes
        #Option :  filter for specific labels or days
        result = []

        for _day in self.notes:
            note = self.notes[_day]

            if day == False or day == _day:

                for _label in note[_day]:

                    if label == False or _label == label:

                        value =  note[_day][_label]
                        result.append({day: _day, label: _label, value:value})

        return result

    def readTodayNote(self, label=False):

        if self.today in self.notes :
            if label == False:
                    return self.notes[self.today]
            else:
                if label in self.notes[self.today]:
                    return self.notes[self.today][label]
                else:
                    return None
        else:
            return None
