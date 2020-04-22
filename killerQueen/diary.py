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

    def nodayNote(self, label, value):
        #Create note unbound to a day
        self.writeNote(0, label, value)

    def readAllNotes(self, label=False, day=False):
        #Return saved notes
        #Option :  filter for specific labels or days
        result = {}

        for _day in self.notes:
            note = self.notes[_day]
            if day == False or day == _day:

                for _label in note:

                    if label == False or _label == label:

                        value =  note[_label]
                        if not _day in result:
                            result[_day] = {}

                        result[_day][_label] = value

        return result


    def readDayNote(self, day = False, label=False):
        #Return note at specific day
        if day in self.notes :
            if label == False:
                    return self.notes[day]
            else:
                if label in self.notes[day]:
                    return self.notes[day][label]
                else:
                    return None
        else:
            return None

    def readTodayNote(self, label=False):
        #Return today's note
        return self.readDayNote(self.today, label)

    def readNodayNote(self, label=False):
        #Return note unbound to a day
        return self.readDayNote(0, label)

    def logNotes(self):
        log(self.notes, json = True)
