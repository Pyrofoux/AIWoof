from .base import *

class POSSESSED(Base):

    def __init__(tracker, diary):
        self.tracker = tracker
        self.diary = diary



    def dayStart(self):

        self.tracker.nextDay()
        self.diary.nextDay()

        self.talkCount = 0
        self.whisperCount = 0

            #POSSESSED disguise as a SEER and does fake divinations
            #Todo : POSSESSED doesn't try to fake divine a SEER

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
