from .base import *

class WEREWOLF(Base):

    def __init__(tracker, diary):
        self.tracker = tracker
        self.diary = diary


    def attack(self):

        target = heatSort(self.tracker, heatAttack)
        self.diary.todayNote("attacked", target)
        return target

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
