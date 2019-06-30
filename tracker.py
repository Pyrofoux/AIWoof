from toolbox import *


#Mapping the corresponding for a role
role2team = {
    "BODYGUARD": 'HUMAN', "MEDIUM": 'HUMAN', "POSSESSED": 'HUMAN', "SEER": 'HUMAN', "FOX": '???', "FREEMASON": '???', "VILLAGER": 'HUMAN', "ANY": '???', "WEREWOLF": 'WEREWOLF'
}


class Tracker(object):

    def __init__(self):

        self.profiles           = {}
        self.gameCompo          = None
        self.totalPlayers       = 0
        self.totalHumanPlayers  = 0
        self.totalAlivePlayers  = 0
        self.totalWolfPlayers   = 0

    def createProfiles(self, baseInfo, gameSetting):
        #Create profiles containing every informations about a player

        #Data contained in game setting and base info
        #gameSetting
        #{"enableNoAttack": false, "enableNoExecution": false, "enableRoleRequest": true, "maxAttackRevote": 1, "maxRevote": 1, "maxSkip": 2, "maxTalk": 10, "maxTalkTurn": 20, "maxWhisper": 10, "maxWhisperTurn": 20, "playerNum": 5, "randomSeed": 8528942025861373791, "roleNumMap": {"BODYGUARD": 0, "MEDIUM": 0, "POSSESSED": 1, "SEER": 1, "FOX": 0, "FREEMASON": 0, "VILLAGER": 2, "ANY": 0, "WEREWOLF": 1}, "talkOnFirstDay": false, "timeLimit": 1000, "validateUtterance": true, "votableInFirstDay": false, "voteVisible": true, "whisperBeforeRevote": false}

        #baseInfo
        #{'agentIdx': 5, 'myRole': 'SEER', 'roleMap': {'5': 'SEER'}, 'day': 0, 'remainTalkMap': {'1': 10, '2': 10, '3': 10, '4': 10, '5': 10}, 'remainWhisperMap': {}, 'statusMap': {'1': 'ALIVE', '2': 'ALIVE', '3': 'ALIVE', '4': 'ALIVE', '5': 'ALIVE'}}


        self.myId = myId = str(baseInfo['agentIdx'])
        self.gameCompo = gameSetting["roleNumMap"]

        #Counting players, humans and wolves
        self.totalPlayers = 0
        for role in self.gameCompo:

            self.totalPlayers += self.gameCompo[role]
            if role2team[role] == "WOLF":
                self.totalWolfPlayers += 1
            else:
                self.totalHumanPlayers += 1
        self.totalAlivePlayers = self.totalPlayers


        for i in range(gameSetting['playerNum']):

            id = str(i+1)


            profile = {}

            profile['id']               = id
            profile['alive']            = True
            profile['talkHistory']      = []

            #Calculated later by updateRoleEstimations
            profile['roleProba']        = None

            if(id == myId):

                profile['role']         = baseInfo['myRole']
                profile['team']         = role2team[profile['role']]
                profile['roleKnown']    = True
                profile['teamKnown']    = True
                profile['isMe']         = True


            else:

                profile['role']         = '???'
                profile['roleKnown']    = False
                profile['team']         = '???'
                profile['teamKnown']    = False
                profile['isMe']         = False


            self.profiles[id] = profile

        self.updateRoleEstimations()

    def update(self, baseInfo, diffData):
        #Updates the profiles according to recent informations

        #Updating alive/dead status
        self.totalAlivePlayers = 0
        for id in baseInfo['statusMap']:
            self.profiles[id]['alive'] = (baseInfo['statusMap'][id] == 'ALIVE')

            if(self.profiles[id]['alive']):
                self.totalAlivePlayers += 1

        #Process every information in diffData
        for index, row in diffData.iterrows():

            #Update divination result
            ## TODO: Implement the consequences on probability of divination
            # if you divine the only wolf, proba -> 1 -> should be sure about the role
            # Idea : check the 1 probability on total of team at the end,
            # Update team if needed, update role if needed
            # If one update was made, recall the probability function
            if row.type == 'divine':

                result = formatDivine(row.text)
                self.profiles[result['id']]['team'] = result['team']
                self.profiles[result['id']]['teamKnown'] = True

                log("DIVINED "+result['id'])

            if row.type == 'talk':
                #log(row)
                True



        self.updateRoleEstimations()
        log(self.profiles, json = 1)
        #log("")



    def updateRoleEstimations(self):

        #Copy the role map given at beginning of the game
        roleMap = dict(self.gameCompo)

        #Initialize empty probability vector
        voidVector = dict(roleMap)
        for role in voidVector:
            voidVector[role] = 0

        #Check the known roles and update roleMap accordingly
        for id in self.profiles:

            profile = self.profiles[id]
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
        for id in self.profiles:

            profile = self.profiles[id]

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


        self.checkRoleDeductions()


    def checkRoleDeductions(self):
    #Deduce team and roles based on probabilities
        didDeductions = False

        for id in self.profiles:

            profile = self.profiles[id]

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
                self.updateRoleEstimations()
