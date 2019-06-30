from toolbox import *

def updateRoleEstimations(tracker):

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
            roleVector = voidVector
            roleVector[profile['role']] = 1
            profile['roleProba'] = roleVector

    #Check unknown roles

    #Count unknown humans and wolves

    unknown = {}
    unknown['WEREWOLF'] = 0
    unknown['HUMAN']    = 0
    unknown['TOTAL']    = 0

    for role in roleMap:

        if role2team[role] == "WEREWOLF":
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

                if(role2team[role] == team):
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

                    team = role2team[role]
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

                    team = role2team[role]
                    profile['roleKnown'] = True
                    profile['role'] = role
                    didDeductions = True


        #If we made deductions, recalculate probabilities
        if didDeductions :
            updateRoleEstimations(tracker)
