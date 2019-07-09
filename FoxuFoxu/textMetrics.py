from toolbox import *
import math


def updateTextMetrics(tracker):
    #Evaluate behavioural metrics based on the way agent talk

    for id in tracker.profiles:

        profile = tracker.profiles[id]

        wolves = tracker.getTeamId('WEREWOLF')
        humans = tracker.getTeamId('HUMAN')
        everybody = tracker.getAllId()

        hostilityPatterns = generateHostilityPatterns(tracker, profile, wolves, humans, everybody, tracker.profiles[tracker.myId])
        profile["hostility"]  = calculateHostility(tracker, profile, hostilityPatterns)
        profile["complexity"] = calculateComplexity(profile)
        #profile[""]



def calculateHostility(tracker, profile, patterns):
    #Evaluates hostility towards our agent
    #... by recognizing hostile or protectives patterns

    if profile['isMe'] :
        return 0
    else:

        hostility = 0
        talks = profile['talkHistory']

        for talk in talks:
            for pattern in patterns:

                text = talk['text']
                day = int(talk['day'])

                occurences = text.count(pattern)
                weight     = patterns[pattern]
                hostility += occurences*weight*day

        hostility = 20/(1+math.exp(-hostility/200))
        return hostility

def calculateComplexity(profile):
    #Evaluates the complexity of agent thoughts
    #... by counting the number of brackets used :D

    texts = getAllTexts(profile)
    maxComplexity = 0
    for text in texts:

        score = text.count("(")
        maxComplexity = max(score, maxComplexity)

    complexity = maxComplexity+1
    return complexity


def generateHostilityPatterns(tracker, profile, wolves, humans, everybody, me):
    #Generate patterns we identify as hostile or cooperative

    myName = formatAgentName(me['id'])
    myRole = me['role']
    myTeam = me['team']

    profileName = formatAgentName(profile['id'])
    profileTeam = profile['team']

    patterns = {}


    if myTeam == "WEREWOLF":
        for id in wolves:

            wolf = formatAgentName(id)

            patterns['ESTIMATE '+wolf+' WEREWOLF'] = 10
            patterns['COMINGOUT '+wolf+' WEREWOLF'] = 10
            patterns['DIVINED '+wolf+' WEREWOLF'] = 30

            patterns['ESTIMATE '+wolf+' POSSESSED'] = 10
            patterns['COMINGOUT '+wolf+' POSSESSED'] = 10

            patterns['ESTIMATE '+wolf+' VILLAGER'] = -10
            patterns['COMINGOUT '+wolf+' VILLAGER'] = -10

            patterns['ESTIMATE '+wolf+' HUMAN'] = -10
            patterns['COMINGOUT '+wolf+' HUMAN'] = -10
            patterns['DIVINED '+wolf+' HUMAN'] = -40 #Someone saying it divined us as HUMAN is lying to protect us

            patterns['VOTE '+wolf] = 15

    elif myTeam == "HUMAN":

        #Coming out as a WEREWOLF is a POSSESSED technique, at a time where killing the wolf is more important
        patterns['COMINGOUT '+profileName+' WEREWOLF'] = -10


        for id in humans:
            human = formatAgentName(id)

            patterns['VOTE '+human] = 5
            patterns['ESTIMATE '+human+' WEREWOLF'] = 5

    if myRole == 'SEER':

        patterns['COMINGOUT '+profileName+' SEER'] = 30

    if myRole == 'MEDIUM':

        patterns['COMINGOUT '+profileName+' MEDIUM'] = 30




    patterns['ESTIMATE '+myName+' WEREWOLF'] = 10
    patterns['COMINGOUT '+myName+' WEREWOLF'] = 10
    patterns['DIVINED '+myName+' WEREWOLF'] = 15

    patterns['ESTIMATE '+myName+' POSSESSED'] = 10
    patterns['COMINGOUT '+myName+' POSSESSED'] = 10

    patterns['ESTIMATE '+myName+' VILLAGER'] = -10
    patterns['COMINGOUT '+myName+' VILLAGER'] = -10

    patterns['ESTIMATE '+myName+' HUMAN'] = -10
    patterns['COMINGOUT '+myName+' HUMAN'] = -10

    patterns['ESTIMATE '+myName+' MEDIUM'] = -10
    patterns['COMINGOUT '+myName+' MEDIUM'] = -10

    patterns['ESTIMATE '+myName+' BODYGUARD'] = -10
    patterns['COMINGOUT '+myName+' BODYGUARD'] = -10

    patterns['VOTE '+myName] = 25

    return patterns


def getAllTexts(profile):

    txts = []
    for talk in profile['talkHistory']:
        txts.append(talk["text"])

    return txts
