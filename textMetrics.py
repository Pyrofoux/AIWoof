from toolbox import *

def updateTextMetrics(tracker):
    #Evaluate behavioural metrics based on the way agent talk

    for id in tracker.profiles:

        profile = tracker.profiles[id]

        profile["hostility"]  = calculateHostility(profile)
        profile["complexity"] = calculateComplexity(profile)



def calculateHostility(profile):
    #Evaluates hostility towards our agent
    #... by recognizing hostile or protectives patterns

    patterns = generateHostilityPatterns()

    if profile['isMe'] :
        return -100
    else:
        return 0

def calculateComplexity(profile):
    #Evaluates the complexity of agent thoughts
    #... by counting the number of brackets used :D
    texts = getAllTexts(profile)
    maxComplexity = 0
    for text in texts:

        score = text.count("(")
        maxComplexity = max(score, maxComplexity)

    return maxComplexity


def generateHostilityPatterns(currentId):
    return None


def getAllTexts(profile):

    txts = []
    for talk in profile['talkHistory']:
        txts.append(talk["text"])

    return txts
