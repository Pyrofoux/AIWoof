from toolbox import *


minimumHeat = float('-inf')
maximumHeat = float('inf')


def heatDivine(id, tracker, profile, roles, myProfile):

    if profile['isMe']:
        return minimumHeat

    if profile['teamKnown']:
        return minimumHeat

    if not profile['alive']:
        return minimumHeat

    rolePriority = roles['WEREWOLF'] * 2 + roles['POSSESSED']
    menace = (profile['hostility']+1)*(profile['complexity']+1)
    heat = rolePriority*menace

    return heat


def heatAttack(id, tracker, profile, roles, myProfile):

    if profile['isMe']:
        return minimumHeat

    if not profile['alive']:
        return minimumHeat

    if profile['teamKnown'] and profile['team'] == 'WEREWOLF':
        return minimumHeat

    rolePriority = roles['SEER']*3 + roles['MEDIUM']*2 + roles['BODYGUARD']*2 + roles['VILLAGER']

    menace = (profile['hostility']+1)*(profile['complexity']+1)
    heat = rolePriority*menace

    return heat

def heatVote(id, tracker, profile, roles, myProfile):

    if profile['isMe']:
        return minimumHeat

    if not profile['alive']:
        return minimumHeat


    rolePriority = 0

    if role2team[myProfile['role']] == 'HUMAN':
        rolePriority = roles['WEREWOLF'] * 2 + roles['POSSESSED']

    else :
        rolePriority = roles['SEER']*3 + roles['MEDIUM']*2 + roles['BODYGUARD']*2 + roles['VILLAGER']

    menace = (profile['hostility']+1)*(profile['complexity']+1)
    heat = rolePriority*menace

    return heat


def heatGuard(id, tracker, profile, roles, myProfile):

    if not profile['alive']:
        return minimumHeat

    if profile['isMe']:
        return maximumHeat

    return 0


def heatSort(tracker, heatFunction):
    #Calculate heat according to heatFunction and return the agent with highest heat

    agentList = []

    myProfile = tracker.profiles[tracker.myId]

    for id in tracker.profiles:

        profile = tracker.profiles[id]
        roles = profile['roleProba']


        couple = {}
        couple['id']    = id
        couple['heat']  = heatFunction(id, tracker, profile, roles, myProfile)
        agentList.append(couple)

    #Random shuffle to avoid always returning smallest id agent if heats are similar
    random.shuffle(agentList)

    agentList.sort(key = lambda couple : couple['heat'], reverse=True)
    targetId = agentList[0]['id']
    return targetId
