Notes for Programming Agents
============================

The aiwolf-py originally developed by [Kei Harada](https://github.com/k-harada/) allows the development of Python agents for the AIWolf competition. This document will briefly describe how you can use this library to develop agents using Python.

First and foremost you must `import aiwolfpy` in your script. Once that is done, you can create a class for your agent and can use the aiwolfpy library to connect to a server by running `aiwolfpy.connect_parse(myAgentObject)`. Once this is run, the aiwolfpy library will connect to the server and will be the intermediary between the server and your agent.

## Agent Class

Your agent class is required to implement a number of functions that will be called by the aiwolfpy library.

`getName(self)`: returns the name of the agent (string)

`initialize(self, base_info, diff_data, game_setting)`: this function is called before a game starts. base_info, diff_data and game_setting contains important information about the current game. The contents of it are described in the next section. Note that this function is different from the __init__ one. Returns `None`.

`dayStart(self)`: called at the start of the day.  Returns `None`.

`talk/whisper(self)`: should return a full sentence according to the protocol in the string format (the content builder can be used to generate valid sentences). Returns `str`.

`vote/attack/divine/guard(self)`: should return an ID (integer) of one of the agents. Returns `int`.

`finish(self)`: called when the game finishes. Returns `None`.

`update(self, base_info, diff_data, request)`: after `initialize` is called and the game starts, the aiwolfpy library always make pair of calls to your agent: first the update function, and then some other function (e.g. talk). The update allows your agent to process new information from the environment, while the second function represents the actual action your agent has to perform at that point of the game. Returns `None`.


## Information received from the server

All information received from the server are either in the format of nested dictionaries or pandas dataframes. 

 * game_setting: contains a number of settings related to the current came as specified the AIWolf server, such as number of players, how many times an agent can talk per day, etc. 

```
game_setting Example:
{
    "maxRevote": 1, 
    "randomSeed": 1548825638306, 
    "validateUtterance": true, 
    "enableNoExecution": false, 
    "roleNumMap": {
        "BODYGUARD": 0, 
        "MEDIUM": 0, 
        "SEER": 1, 
        "WEREWOLF": 1, 
        "POSSESSED": 1, 
        "VILLAGER": 2, 
        "FOX": 0, 
        "FREEMASON": 0
    }, 
    "votableInFirstDay": false, 
    "maxSkip": 2, 
    "timeLimit": -1, 
    "maxWhisper": 10, 
    "maxWhisperTurn": 20, 
    "whisperBeforeRevote": false, 
    "maxTalkTurn": 20, 
    "playerNum": 5, 
    "voteVisible": true, 
    "maxAttackRevote": 1, 
    "talkOnFirstDay": false, 
    "enableNoAttack": false, 
    "maxTalk": 10
}
```

* base_info: contains basic information available to your agent at the current state of the game.
<!--- 
I don't think this individual explanation is necessary but for now let's leave it commented out
	* agentIdx: your agent ID (`int` format)
	* `statusMap`: contains the status ("DEAD" or "ALIVE") of each agent. It's a dictionary with pairs of key values in the format ID - Status. Note that ID is in `str` format
	* `remainTalkMap`: how many more sentences the agent can issue at the current state of the current phase.  Note that ID is in `str` format
	* `remainWhisperMap`: similar to previous one, in this case for Werewolf during the night phase.  Note that ID is in `str` format
	* `roleMap`: when a werewolf, you can identify other werewolf places from this dictionary.  Note that ID is in `str` format
	* `myRole`: your role in the current game in `str` format
	* `day`: the current day of the game (`int` format)
 --->
 ```
 # base_info Example:
 {
    "agentIdx": 5, 
    "statusMap": {
        "1": "ALIVE", 
        "3": "ALIVE", 
        "2": "ALIVE", 
        "5": "DEAD", 
        "4": "ALIVE"
    }, 
    "remainTalkMap": {		# How many statements each agent can still issue at the current turn
        "1": 10, 
        "3": 10, 
        "2": 10, 
        "4": 10
    }, 
    "remainWhisperMap": {}, 	# same as remainTalkMap, but in the case of whisper for werewolves
    "roleMap": {  		# when a werewolf, use this dict to find other werewolves
        "5": "WEREWOLF"
    }, 
    "myRole": "WEREWOLF", 
    "day": 2
}
```
 
 * diff_data: A pandas dataframe that contains every new information since last communication with server. The `idx` header represents the order in which the events occurred.
 
 ```
diff_data Example:
+----+---------+-------+-------+-----------------------------+--------+--------+
|    |   agent |   day |   idx | text                        |   turn | type   |
|----+---------+-------+-------+-----------------------------+--------+--------|
|  0 |       2 |     1 |    10 | Skip                        |      2 | talk   |
|  1 |       4 |     1 |    11 | ESTIMATE Agent[05] WEREWOLF |      2 | talk   |
|  2 |       5 |     1 |    12 | VOTE Agent[02]              |      2 | talk   |
|  3 |       3 |     1 |    13 | Skip                        |      2 | talk   |
|  4 |       1 |     1 |    14 | DIVINED Agent[04] HUMAN     |      2 | talk   |
+----+---------+-------+-------+-----------------------------+--------+--------+
 ```
 
## Content builder

The content builder file within the aiwolfpy library allows the generation of valid sentences according to the AIWolf protocol specification.

The following functions are provided by aiwolfpy (ordered according to the protocol specification document): 

* 2.1 Sentences that express knowledge or intent

	* `estimate/comingout(target, role)`: passes a target id (type `int`) and a role (type `str`), returns a sentence in the format: ```ESTIMATE Agent[0] WEREWOLF```

* 2.2 Sentences about actions of the Werewolf game

	* `divine/guard/vote/attack(target)`: passes a target id (type `int`), returns a sentence in the format: ```DIVINE Agent[0] ```

* 2.3 Sentences about the result of past actions

	* `divined/identified(target, species)`: passes a target id (type `int`) and a species (type `str`), returns a sentence in the format: ```DIVINED Agent[0] HUMAN ```

	* `guarded(target)`: passes a target id (type `int`), returns a sentence of type ```GUARDED Agent[0] ```

* 2.4 Sentences that express agreement or disagreement

	* `agree/disagree(talktype, day, id)`: passes a talktype (????), a day (type `int`) and an id (type `str`), returns a sentence in the format: ```AGREE talktype Day day ID: id```

* 2.5 Sentences related to the flow of the conversation

	* `skip/over()`: no parameter required, simply returns `Skip` or `Over`.

* 3 Operators for directed requests of action and information

	* `request(text)`: passes a sentence built with one of the previous functions, and returns a sentence in the format: `REQUEST (text)`
 
