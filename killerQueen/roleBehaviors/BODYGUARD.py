from .base import *

class BODYGUARD(Base):

    def __init__(tracker, diary):
        self.tracker = tracker
        self.diary = diary


    def guard(self):
    #only BODYGUARD can guard
        target = heatSort(self.tracker, heatGuard)
        self.diary.todayNote("guarded", target)
        return target
