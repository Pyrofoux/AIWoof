from toolbox import *

def updateTextMetrics(tracker):
    #Evaluate behavioural metrics based on the way agent talk

    for id in tracker.profiles:

        profile = tracker.profiles[id]

        hostilityPatterns = generateHostilityPatterns(tracker.myId)
        profile["hostility"]  = calculateHostility(profile, hostilityPatterns)
        profile["complexity"] = calculateComplexity(profile)
        #profile[""]



def calculateHostility(profile, patterns):
    #Evaluates hostility towards our agent
    #... by recognizing hostile or protectives patterns

    if profile['isMe'] :
        return -100
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

        return hostility

def calculateComplexity(profile):
    #Evaluates the complexity of agent thoughts
    #... by counting the number of brackets used :D

    texts = getAllTexts(profile)
    maxComplexity = 0
    for text in texts:

        score = text.count("(")
        maxComplexity = max(score, maxComplexity)

    return maxComplexity


def generateHostilityPatterns(myId):

    myName = formatAgentName(myId)

    patterns = {}


    patterns['ESTIMATE '+myName+' WEREWOLF'] = 10
    patterns['COMINGOUT '+myName+' WEREWOLF'] = 10
    patterns['DIVINED '+myName+' WEREWOLF'] = 15

    patterns['ESTIMATE '+myName+' POSSESSED'] = 10
    patterns['COMINGOUT '+myName+' POSSESSED'] = 10
    patterns['DIVINED '+myName+' POSSESSED'] = 15

    patterns['ESTIMATE '+myName+' VILLAGER'] = -10
    patterns['COMINGOUT '+myName+' VILLAGER'] = -10
    patterns['DIVINED '+myName+' VILLAGER'] = -15

    patterns['ESTIMATE '+myName+' HUMAN'] = -10
    patterns['COMINGOUT '+myName+' HUMAN'] = -10
    patterns['DIVINED '+myName+' HUMAN'] = -15

    patterns['ESTIMATE '+myName+' MEDIUM'] = -10
    patterns['COMINGOUT '+myName+' MEDIUM'] = -10
    patterns['DIVINED '+myName+' MEDIUM'] = -15

    patterns['VOTE '+myName] = 20




    return patterns


def getAllTexts(profile):

    txts = []
    for talk in profile['talkHistory']:
        txts.append(talk["text"])

    return txts
