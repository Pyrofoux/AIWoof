from .base import *

class SEER(Base):

    def __init__(tracker, diary):
        self.tracker = tracker
        self.diary = diary

    def talk(self):

        self.talkCount += 1

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

        return cb.skip()


    def divine(self):
        #Only SEER can divine
        target = heatSort(self.tracker, heatDivine)
        self.diary.todayNote("guarded", target)
        return target
