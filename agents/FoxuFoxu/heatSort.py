from toolbox import *


minimumHeat = -999999999999999
maximumHeat = +999999999999999


def heatDivine(id, tracker, profile, roles, myProfile):

    if profile['isMe']:
        return minimumHeat

    if profile['teamKnown']:
        return minimumHeat

    if not profile['alive']:
        return minimumHeat

    rolePriority = roles['WEREWOLF'] * 2 + roles['POSSESSED'] - roles['VILLAGER'] -2*roles['MEDIUM'] -2*roles['BODYGUARD']
    menace = profile['hostility']*profile['complexity']
    heat = rolePriority*menace

    return heat


def heatAttack(id, tracker, profile, roles, myProfile):

    if profile['isMe']:
        return minimumHeat

    if not profile['alive']:
        return minimumHeat

    if profile['team'] == 'WEREWOLF':
        return minimumHeat

    rolePriority = roles['SEER']*3 + roles['MEDIUM']*2 + roles['BODYGUARD']*2 + roles['VILLAGER'] - roles['POSSESSED'] -2*roles['WEREWOLF']

    menace = profile['hostility']*profile['complexity']
    heat = rolePriority*menace

    return heat

def heatVote(id, tracker, profile, roles, myProfile):

    if profile['isMe']:
        return minimumHeat

    if not profile['alive']:
        return minimumHeat


    rolePriority = 0

    if role2team[myProfile['role']] == 'HUMAN':
        rolePriority = roles['WEREWOLF'] * 2 + roles['POSSESSED'] - roles['VILLAGER'] -2*roles['MEDIUM'] -2*roles['BODYGUARD']


    else :
        rolePriority = roles['SEER']*3 + roles['MEDIUM']*2 + roles['BODYGUARD']*2 + roles['VILLAGER'] - roles['POSSESSED'] -2*roles['WEREWOLF']

    menace = profile['hostility']*profile['complexity']
    heat = rolePriority*menace

    return heat


def heatGuard(id, tracker, profile, roles, myProfile):

    if not profile['alive']:
        return minimumHeat


    if tracker.totalAlivePlayers <= 0.5*tracker.totalPlayers:

        rolePriority = roles['SEER']*3 + roles['MEDIUM']*2 + roles['BODYGUARD']*2 + roles['VILLAGER'] - roles['POSSESSED'] -2*roles['WEREWOLF']
        menace = profile['hostility']*profile['complexity']
        heat = rolePriority*menace

        return heat

    if profile['isMe']:
        return maximumHeat

    return 0


def heatMap(tracker, heatFunction):
    #Calculate heat of agents according to heatFunction
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

    return agentList

def heatSort(tracker, heatFunction):
    #Calculate heat according to heatFunction and return the agent with highest heat

    sortedHeat = heatMap(tracker, heatFunction)
    targetId = sortedHeat[0]['id']
    return targetId


def getHeat(id, map):

    for agent in map:
        if int(agent['id']) == id:
            return agent['heat']
    return None
