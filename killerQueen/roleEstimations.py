from __future__ import division
from toolbox import *


def updateRoleEstimations(tracker):

    #Copy the role map given at beginning of the game, calculate the team map
    roleMap = dict(tracker.gameCompo)
    teamMap = countTeam(roleMap)

    #Initialize empty probability vector
    voidRoleVector = dict(roleMap)
    for role in voidRoleVector:
        voidRoleVector[role] = 0

    voidTeamVector = {'HUMAN':0, 'WEREWOLF':0}

    #Set probabilities when role is known
    #+ remove known roles from current maps
    for id in tracker.profiles:

        profile = tracker.profiles[id]

        if profile['roleKnown'] and profile['teamKnown']:

            role = profile['role']
            team = role2divined[role] #Important: We consider teams given by a divined action

            #1 for the role, 0 for the other
            roleVector = dict(voidRoleVector)
            roleVector[role] = 1
            profile['roleProba'] = roleVector

            #1 for the team, 0 for the other
            teamVector = dict(voidTeamVector)
            teamVector[team] = 1
            profile['teamProba'] = teamVector

            #remove role and team from the list of unknown attributions
            roleMap[role] -= 1
            teamMap[team] -= 1


    for id in tracker.profiles:

        profile = tracker.profiles[id]

        if not profile['roleKnown'] and profile['teamKnown']:

            team = profile['team']

            #Counting the reamining roles for the known team
            roleVector   = filterTeam(roleMap, team)
            totalTeam    =  totalDict(roleVector)

            for role in roleVector:
                number = roleVector[role]

                #Avoid dividing by zero
                if number == 0 or totalTeam == 0:
                    roleVector[role] = 0
                else:
                #Probability of being this role, knowing we're in the current team
                    roleVector[role] = number / totalTeam

            profile['roleProba'] = roleVector

            teamVector = dict(voidTeamVector)
            teamVector[team] = 1
            profile['teamProba'] = teamVector

            #Remove team member from the list of unknown team attributions
            teamMap[team] -= 1

    #Calculate probabilities when role is unknown
    for id in tracker.profiles:

        profile = tracker.profiles[id]

        if not profile['roleKnown'] and not profile['teamKnown']:

            teamVector = {'HUMAN': 0,'WEREWOLF': 0}
            totalTeam = totalDict(teamMap)

            if totalTeam > 0:
                teamVector['WEREWOLF'] = teamMap['WEREWOLF']/totalTeam
                teamVector['HUMAN'] = teamMap['HUMAN']/totalTeam

            conditionalRoleVector = {}
            conditionalRoleVector['HUMAN']      = filterTeam(roleMap, 'HUMAN')
            conditionalRoleVector['WEREWOLF']   = filterTeam(roleMap, 'WEREWOLF')

            totalRoleMap = totalDict(roleMap)

            for team in conditionalRoleVector:
                for role in conditionalRoleVector[team]:
                    conditionalRoleVector[team][role] /= totalRoleMap

            roleVector = dict(voidRoleVector)

            for role in roleVector:
                for team in teamVector:
                    #Bayesian probability
                    roleVector[role] += conditionalRoleVector[team][role]*teamVector[team]

            profile['teamProba'] = teamVector
            profile['roleProba'] = roleVector


    checkRoleDeductions(tracker)

def countTeam(roleMap):
    #Count number of humans and wolves in a role map
    teamMap = {'HUMAN':0, 'WEREWOLF':0}

    for role in roleMap:
        team = role2divined[role]
        if team in teamMap:
            teamMap[team] += roleMap[role]

    return teamMap

def filterTeam(roleMap, team):
    #Keep only the roles from a specific team in a role map
    filtered = dict(roleMap)

    for role in filtered:
        if not role2divined[role] == team:
            filtered[role] = 0

    return filtered


def checkRoleDeductions(tracker):
#Deduce team and roles based on probabilities
    didDeductions = False

    for id in tracker.profiles:

        profile = tracker.profiles[id]

        #Check if we can guess the team based on probabilities
        if profile['teamKnown'] == False:

            for team in profile['teamProba']:

                if(profile['teamProba'][team] == 1):

                    profile['team'] = team
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
