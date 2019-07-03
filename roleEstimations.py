from toolbox import *


def updateRoleEstimations(tracker):

    #Copy the role map given at beginning of the game, calculate the team map
    roleMap = dict(tracker.gameCompo)

    #Initialize empty probability vector
    voidRoleVector = dict(roleMap)
    for role in voidVector:
        voidVector[role] = 0

    voidTeamVector = {'HUMAN':0, 'WEREWOLF':0}

    #Set probabilities when role is known
    #+ remove known roles from current maps
    for id in tracker.profiles:

        profile = tracker.profiles[id]

        if profile['roleKnown'] :

            role = profile['role']
            team = role2divined[role]

            roleVector = dict(voidRoleVector)
            roleVector[role] = 1
            profile['roleProba'] = roleVector

            teamVector = dict(voidTeamVector)
            teamVector[team] = 1
            profile['teamProba'] = roleVector

            roleMap[role] -= 1
            teamMap[team] -= 1

    #Set probabilities when role is known
    #+ remove known roles from current team map

    teamMap = countTeam(roleMap)

        for id in tracker.profiles:

            profile = tracker.profiles[id]

            if profile['roleKnown'] :

                team = profile['team']

                roleVector = dict(voidRoleVector)
                roleVector[role] = 1
                profile['roleProba'] = roleVector

                teamVector = dict(voidTeamVector)
                teamVector[team] = 1
                profile['teamProba'] = roleVector

                roleMap[role] -= 1
                teamMap[team] -= 1

    #Count unknown humans and wolves

    unknown = {}
    unknown['WEREWOLF'] = 0
    unknown['HUMAN']    = 0
    unknown['TOTAL']    = 0

    for role in roleMap:

        if role2divined[role] == "WEREWOLF":
            unknown['WEREWOLF'] += roleMap[role]
        else :
            unknown['HUMAN'] += roleMap[role]

        unknown["TOTAL"] += roleMap[role]


    #Calculate probabilities
    for id in tracker.profiles:

        profile = tracker.profiles[id]

        #If we have info about their team
        if profile['teamKnown'] :

            if(profile['roleKnown']): #Only check unnown roles
                continue

            team = profile['team']
            roleVector = dict(roleMap)

            for role in roleMap:

                if(role2divined[role] == team):
                    roleVector[role] /= unknown[team]
                else:
                    roleVector[role] = 0

        #If we don't have info about their team
        else:

            roleVector = dict(roleMap)
            for role in roleMap:
                roleVector[role] /= unknown["TOTAL"]

        profile['roleProba'] = roleVector


    checkRoleDeductions(tracker)

def countTeam(roleMap):
    #Count number of humans and wolves in a role map
    teamMap = {'HUMAN':0, 'WEREWOLF':0}

    for role in roleMap:
        teamMap[role2divined[role]] += 1

    return teamMap

def filterTeam(roleMap, team):
    #Keep only the roles from a specific team in a role map
    filtered = dict(roleMap)

    for role in filtered:
        if not role2divined[role] == team:
            filtered[role] = 0

    return filtered



def updateRoleEstimationsOld(tracker):

    #Copy the role map given at beginning of the game
    roleMap = dict(tracker.gameCompo)

    #Initialize empty probability vector
    voidVector = dict(roleMap)
    for role in voidVector:
        voidVector[role] = 0

    #Check the known roles and update roleMap accordingly
    for id in tracker.profiles:

        profile = tracker.profiles[id]
        if profile['roleKnown'] :

            roleMap[profile['role']] -= 1
            roleVector = dict(voidVector)
            roleVector[profile['role']] = 1
            profile['roleProba'] = roleVector

    #Check unknown roles

    #Count unknown humans and wolves

    unknown = {}
    unknown['WEREWOLF'] = 0
    unknown['HUMAN']    = 0
    unknown['TOTAL']    = 0

    for role in roleMap:

        if role2divined[role] == "WEREWOLF":
            unknown['WEREWOLF'] += roleMap[role]
        else :
            unknown['HUMAN'] += roleMap[role]

        unknown["TOTAL"] += roleMap[role]


    #Calculate probabilities
    for id in tracker.profiles:

        profile = tracker.profiles[id]

        #If we have info about their team
        if profile['teamKnown'] :

            if(profile['roleKnown']): #Only check unnown roles
                continue

            team = profile['team']
            roleVector = dict(roleMap)

            for role in roleMap:

                if(role2divined[role] == team):
                    roleVector[role] /= unknown[team]
                else:
                    roleVector[role] = 0

        #If we don't have info about their team
        else:

            roleVector = dict(roleMap)
            for role in roleMap:
                roleVector[role] /= unknown["TOTAL"]

        profile['roleProba'] = roleVector


    checkRoleDeductions(tracker)


def checkRoleDeductions(tracker):
#Deduce team and roles based on probabilities
    didDeductions = False

    for id in tracker.profiles:

        profile = tracker.profiles[id]

        #Check if we can guess the team based on probabilities
        if profile['teamKnown'] == False:

            possibleTeams = []

            for role in profile['roleProba']:

                if profile['roleProba'][role] > 0:

                    team = role2divined[role]
                    if not (team in possibleTeams):
                        possibleTeams.append(team)

            #Deducted team
            if len(possibleTeams) == 1:
                profile['team'] = possibleTeams[0]
                profile['teamKnown'] = True
                didDeductions = True

        #Check if we can guess the role  based on probabilities
        if profile['roleKnown'] == False:

            for role in profile['roleProba']:

                #Deducted team
                if profile['roleProba'][role] == 1:

                    team = role2divined[role]
                    profile['roleKnown'] = True
                    profile['role'] = role
                    didDeductions = True


        #If we made deductions, recalculate probabilities
        if didDeductions :
            updateRoleEstimations(tracker)
