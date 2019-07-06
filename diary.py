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

    def addNote(self, day, label, value):
        #Creates a note for given day, with specific label
        day = int(day)

        if day in self.notes:
            self.notes[day] = []

        self.notes[day][label] = value

    def todayNote(self, label, value):
        #Creates note at current day
        self.addNote(self.today, label, value)


    def readAllNotes(self, specificLabel=False, specificDay=False):
        #Return saved notes
        #Option :  filter for specific labels or days
        result = []

        for day in self.notes:
            note = self.notes[day]

            if specificDay == False or specificDay == day:

                for label in note[day]:

                    if specificLabel == False or specificLabel == day:

                        value =  note[day][label]
                        result.append({day: day, label: label, value:value})

        return result
