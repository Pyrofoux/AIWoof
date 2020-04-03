from toolbox import *
from roleEstimations import *
from textMetrics import *



class Tracker(object):

    def __init__(self):

        self.profiles           = {}
        self.gameCompo          = None
        self.totalPlayers       = 0
        self.totalHumanPlayers  = 0
        self.totalAlivePlayers  = 0
        self.totalWolfPlayers   = 0

        self.currentDay         = 0
        self.myId               = 0
        self.myRole             = "ANY"

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
            if role2divined[role] == "WOLF":
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
            profile['hostility']        = 0
            profile['complexity']       = 0

            #Calculated later by updateRoleEstimations
            profile['roleProba']        = None
            profile['teamProba']        = None

            if(id == myId):

                profile['role']         = baseInfo['myRole']
                profile['team']         = role2divined[profile['role']]
                profile['roleKnown']    = True
                profile['teamKnown']    = True
                profile['isMe']         = True

                self.myRole             = baseInfo['myRole']


            else:

                profile['isMe']         = False

                if id in baseInfo['roleMap']:

                    profile['role']         = baseInfo['roleMap'][id]
                    profile['roleKnown']    = True
                    profile['team']         = role2divined[profile['role']]
                    profile['teamKnown']    = True

                else:
                    profile['role']         = '???'
                    profile['roleKnown']    = False
                    profile['team']         = '???'
                    profile['teamKnown']    = False



            self.profiles[id] = profile

        updateRoleEstimations(self)

    def update(self, baseInfo, diffData, diary):
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
            ## TODO: Implement more complex probability calculator
            #Eg: If you divined 3 HUMAN, and there are only 3
            # The rest is WEREWOLF
            # + If someone is team WEREWOLF, and there's only one role -> they are that role
            #
            if row.type == 'divine':

                result = formatDivine(row.text)
                self.profiles[result['id']]['team'] = result['team']
                self.profiles[result['id']]['teamKnown'] = True

                diary.todayNote('divined',{'id':result['id'] ,'team': result['team']})

                if result['team'] == 'WEREWOLF':
                    diary.nodayNote('seenWolf', True)


            elif row.type == 'identify':

                result = formatDivine(row.text)
                self.profiles[result['id']]['team'] = result['team']
                self.profiles[result['id']]['teamKnown'] = True

                diary.todayNote('identified',{'id':result['id'] ,'team': result['team']})

                if result['team'] == 'WEREWOLF':
                    diary.nodayNote('seenWolf', True)

            elif row.type == 'talk':

                #Don't read the Skip and Over
                if not row.text in ["Over", "Skip"]:
                    id = str(row.agent)
                    talk = {}
                    talk['day']     = row.day
                    talk['text']    = row.text
                    talk['turn']    = row.turn
                    talk['id']      = row.idx

                    self.profiles[id]['talkHistory'].append(talk)

            elif row.type == 'dead':

                #We consider agents dead in the night as HUMAN for now
                id = str(row.agent)
                profile = self.profiles[id]

                if profile['teamKnown'] == False:

                    profile['team'] = 'HUMAN'
                    profile['teamKnown'] = True

            elif row.type == 'vote':
                None

        updateRoleEstimations(self)
        updateTextMetrics(self)


    def getTeamId(self, team):

        list = []
        for id in self.profiles:

            profile = self.profiles[id]
            if(profile['team'] == team):
                list.append(id)
        return list

    def getAllId(self):

        list = []
        for id in self.profiles:

            profile = self.profiles[id]
            list.append(id)
        return list


    def nextDay(self):
        self.currentDay += 1


    def printProfiles(self):

        for id in self.profiles:

            profile = dict(self.profiles[id])
            del profile['talkHistory']

            log(profile, json = True)
