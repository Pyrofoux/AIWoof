from toolbox import *


role2team = {
    "BODYGUARD": 'HUMAN', "MEDIUM": 'HUMAN', "POSSESSED": 'HUMAN', "SEER": 'HUMAN', "FOX": '???', "FREEMASON": '???', "VILLAGER": 'HUMAN', "ANY": '???', "WEREWOLF": 'WEREWOLF'
}


class Tracker(object):

    def __init__(self):

        self.profiles           = {}
        self.gameCompo          = None
        self.totalPlayers       = None
        self.totalAlivePlayers  = None

    def createProfiles(self, baseInfo, gameSetting):

        #gameSetting
        #{"enableNoAttack": false, "enableNoExecution": false, "enableRoleRequest": true, "maxAttackRevote": 1, "maxRevote": 1, "maxSkip": 2, "maxTalk": 10, "maxTalkTurn": 20, "maxWhisper": 10, "maxWhisperTurn": 20, "playerNum": 5, "randomSeed": 8528942025861373791, "roleNumMap": {"BODYGUARD": 0, "MEDIUM": 0, "POSSESSED": 1, "SEER": 1, "FOX": 0, "FREEMASON": 0, "VILLAGER": 2, "ANY": 0, "WEREWOLF": 1}, "talkOnFirstDay": false, "timeLimit": 1000, "validateUtterance": true, "votableInFirstDay": false, "voteVisible": true, "whisperBeforeRevote": false}

        #baseInfo
        #{'agentIdx': 5, 'myRole': 'SEER', 'roleMap': {'5': 'SEER'}, 'day': 0, 'remainTalkMap': {'1': 10, '2': 10, '3': 10, '4': 10, '5': 10}, 'remainWhisperMap': {}, 'statusMap': {'1': 'ALIVE', '2': 'ALIVE', '3': 'ALIVE', '4': 'ALIVE', '5': 'ALIVE'}}


        self.myId = myId = str(baseInfo['agentIdx'])
        self.gameCompo = gameSetting["roleNumMap"]

        for i in range(gameSetting['playerNum']):

            id = str(i+1)


            profile = {}

            profile['id']               = id
            profile['alive']            = True
            profile['talkHistory']      = []

            #Calculated later
            profile['roleProba']        = None

            if(id == myId):

                profile['role']         = baseInfo['myRole']
                profile['roleKnown']    = True
                profile['teamKnown']    = True
                profile['isMe']         = True


            else:

                profile['role']         = '???'
                profile['roleKnown']    = False
                profile['team']         = '???'
                profile['teamKnown']    = True
                profile['isMe']         = False


            self.profiles[id] = profile

        self.updateRoleEstimations()

    def update(self, baseInfo, diffData):


        #Updating alive status
        for id in baseInfo['statusMap']:
            self.profiles[id]['alive'] = (baseInfo['statusMap'][id] == 'ALIVE')

        for index, row in diffData.iterrows():

            True
            #if row.type == 'divine':
        return False



    def updateRoleEstimations(self):


        roleMap = dict(self.gameCompo)

        #Initialize empty probability vector
        voidVector = dict(roleMap)
        for role in voidVector:
            voidVector[role] = 0

        #Check the known roles
        for id in self.profiles:

            profile = self.profiles[id]
            if profile['roleKnown'] :

                roleMap[profile['role']] -= 1
                roleVector = voidVector
                roleVector[profile['role']] = 1
                profile['roleProba'] = roleVector

            elif profile['teamKnown'] :
                None

            else:
                
