from toolbox import *

def heatDivine(id, tracker):
    None


def heatAttack(id, tracker):
    None

def heatVote(id, tracker):
    None


def heatGuard(id, tracker):
    None


def heatSort(tracker, heatFunction):

    agentList = []
    for id in tracker.profiles:

        couple = {}
        couple['id']    = id
        couple['heat']  = heatFunction(id, tracker)
        agentList.append(couple)

    sortedAgentList = agentList.sort(key = lambda couple : couple.heat)
    targetId = sortedAgentList[0].id
    return targetId
