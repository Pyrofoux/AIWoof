AIWolf Protocol Specification
=============================
(Ver 3.6, 2019, English Translation, For AIWolf server version 5)
Original Authors: Osawa, Otsuki, English Translation: Hauck, Aranha

This file describes the specification for the AIWolf Protocol used in the
AIWolf Competition Protocol Division. This file includes valid words,
verbs and rules for sentence construction, as well as notes on how to interpret
constructed sentences.

# Words:
A word is a unit of meaning. It can be one of the following:

- [subject]: an agent identifier (ex: Agent1), or UNSPEC (ommited), or ANY
- [target]: an agent identifier, or ANY (undefined)
- [role]: one of the 6 valid roles (VILLAGER, SEER, MEDIUM, BODYGUARD, WEREWOLF, POSSESSED) or ANY
- [species]: one of the 2 valid teams (HUMAN, WEREWOLF) or ANY
- [verb]: one of 15 valid verbs (specified below)
- [talk number]: unique id for each sentence (composed of [day number] and [talk id])

If ANY is specified for any of [subject][target][role][species], it means that
it can refers to any of the valid options in each set of
[subject][target][role][species].

# Sentence:
There are 13 types of sentence. Each sentence is composed of multiple words.

## Sentences that express knowledge or intent (2 types)
- [subject] ESTIMATE [target] [role]: The [subject] suggests that the [target]’s role is [role]
- [subject] COMINGOUT[target] [role]: The [subject] states that the [target]’s role is [role]

## Sentences about actions of the Werewolf game (4 types)
- [subject] DIVINATION [target]: The [subject] divines the [target]
- [subject] GUARD [target]: The [subject] guards the [target]
- [subject] VOTE [target]: The [subject] votes on the [target]
- [subject] ATTACK [target]: The [subject] attacks the [target]

## Sentences about the result of past actions (5 types)

- [subject] DIVINED [target][species]:
	The [subject] used the seer’s action on living [target] and obtained the result [species]
- [subject] IDENTIFIED [target][species]:
	The [subject] used the medium’s action on dead [target] and obtained the result [species]
- [subject] GUARDED [target]: The [subject] guarded the [target]
- [subject] VOTED [target]: The [subject] voted on the [target]
- [subject] ATTACKED [target]: The [subject] attacked the [target]

## Sentences that express agreement or disagreement (2 types)

- [subject] AGREE [talk number]
- [subject] DISAGREE [talk number]

## Sentences related to the flow of the conversation (2 types)

- OVER: “I have nothing else to say” – implies agreement to terminate current day of conversation
- SKIP: “I have nothing to say now” – implies desire to continue the current day of conversation

NOTE: The two sentences above can only be used as single statements, never nested in other statements.

# Operator:
There are 8 types of operators. Each operator is used to frame sentences and express their relationships.

## Operators for directed requests of action and information (2 types)
- [subject] REQUEST [target] ([sentence]):
	[subject] requests that [target] acts according to [sentence], or acts so that the state of [sentence] is achieved. If the sentence uses ANY in its composition, then any appropriate expansion of ANY is acceptable as the object of the REQUEST.
- [subject] INQUIRE [target] ([sentence]):
	[subject] questions [target] about [sentence]. If ANY is not used in the sentence, [target] is simply being asked if it agrees with the sentence or not. If ANY is used in the sentence, [target] is being asked to reply with the appropriate word to replace ANY.

## Reasoning Operators (1 type)
- [subject] BECAUSE ([sentence1]) ([sentence2])
- [subject] states that [sentence1] is the reason for [sentence2]

## Time indication Operators (1 type)
- [subject] DAY [day_number] ([sentence]): Subject indicates that [sentence] took place on [day_number]. (Note: Good for using along with BECAUSE)

## Logic Operators: (4 types)
- [subject] NOT ([sentence]): Negate the [sentence]
- [subject] AND ([sentence1])([sentence2])([sentence3])…: Claims that all sentences are true
- [subject] OR ([sentence1])([sentence2])([sentence3])…: Claims that at least one sentence is true.
- [subject] XOR ([sentence1])([sentence2]): Claims that either sentence1 or sentence 2 is true.

# Grammar Notes:
- An agent’s statement can be composed of one or more sentences.
- More than one sentences can be separated by parentheses
- Sentences can be prefaced by an operator.
- The type of operator defines what type of word or sentence should follow it.
- Sentences following an operator should be delimited by parenthesis.

## About omitting subjects (UNSPEC)

It is possible to omit the [subject] of a sentence (using UNSPEC). In cases
where omitting the [subject] does not change the meaning of the sentence, we
recommend that the [subject] is omitted. However, note that every agent should
be able to interpret sentences in full or shortened format.

When [subject] is omitted, if the sentence is in the widest scope (when the
sentence comes at the beginning of the agent’s statement), the omitted [subject]
should be interpreted to be the same as the speaking agent. If the [subject] is
in a sentence on a narrower scope (a nested sentence), the interpretation of the
omitted [subject] depends on the type of the parent sentence.

REQUEST, INQUIRE: omitted [subject] is to be interpreted to be the same as the
[target] of the parent sentence. Other cases: omitted [subject] is to be
interpreted to be the same as the [subject] of the parent sentence.

# Example Sentences

- “COMINGOUT Agent1 SEER”: The speaker declares that Agent1 is a seer.
- “Agent1 COMINGOUT Agent1 SEER”: Agent1 declares that Agent1 is a seer.
- “DIVINED Agent1 HUMAN”: The speaker has at some point used the seer’s ability on Agent1, and  obtained the “Human” result.
- “Agent1 DIVINED Agent2 WEREWOLF”: Agent1 has at some point used the seer’s ability on Agent2, and obtained the “Werewolf” result.
- “REQUEST Agent2 (DIVINATION Agent3)”: The speaker desires that Agent2 uses the seer’s ability on Agent3. (Note, this is identical to “REQUEST Agent2 (Agent2 DIVINATION Agent3)”
- “GUARD Agent2”: The speaker will use the Bodyguard’s ability on Agent2
- “Agent1 REQUEST Agent2 (GUARD Agent3)”: Agent1 desires that Agent2 uses the Bodyguard Role’s ability on Agent3.

## Interpretation of REQUEST sentences:

### Requesting the agreement of other agents:

“REQUEST Agent1 (ESTIMATE Agent2 [role])”: The speaker is asking that Agent1 change their mind about Agent2, and consider them to be [role]. (Ex: Alice, would you consider that Bob might be a Werewolf?)

“REQUEST ANY (ESTIMATE Agent1 [role])”: The speaker is asking that anyone change their mind about Agent1, and consider them to be [role]. (Ex: Everyone! You should believe that Anna is a Werewolf!)

“REQUEST Agent1 (COMINGOUT Agent2 [role])”: The speaker requests that agent1 declares agent2 to be [role]. This is particularly useful when werewolves are discussing strategy during the night negotiation period.

“REQUEST ANY (COMINGOUT Agent1 [role])”: The speaker requests that someone declare agent1 to be [role]. This is particularly useful when werewolves are discussing strategy during the night negotiation period.

### Requesting game actions:

“REQUEST Agent1 (DIVINATION Agent2)”: The speaker requests that Agent1 uses the Seers’ divination action on Agent2.

“REQUEST ANY (DIVINATION Agent1)”: The speaker requests that anyone who is a Seer to use their divination action on Agent1

“REQUEST Agent1 (GUARD Agent2)”: The speaker requests that Agent1 uses the Bodyguard’s protection ability on Agent2

“REQUEST ANY (GUARD Agent1)”: The speaker requests that anyone who is a Bodyguard to use their protection ability on Agent1

“REQUEST ANY (VOTE Agent1)”: The speaker request that anyone vote on Agent1 (ex: Let’s all vote on agent1!)

“REQUEST Agent1 (ATTACK Agent2)”: The speaker request that Agent1 uses the werewolf kill ability on Agent2. This is particularly useful when werewolves are discussing strategy during the night negotiation period.

### Requesting an assumed result of actions:

“REQUEST Agent1 (DIVINED Agent2 [species])”

“REQUEST Agent1 (GUARDED Agent2)

“REQUEST ANY (IDENTIFIED Agent1 [species])”

In these sentences, the speaker is requesting that Agent 1 (or any agent, in the last case) behave as if they had performed and received the respective result for a role’s special action (Divined, Guarded, or Identified). This is particularly useful for werewolves who wish to coordinate lies about having particular roles during the night negotiation period. (Ex: “Agent2, you should pretend that you are a Seer, and that you divined that Agent1 (Me) is a Villager”).

### Examples of agreement request:

“REQUEST Agent1 (AGREE [talk number])”: Speaker is requesting that Agent1 agree with the statement specified by [talk number].

“REQUEST ANY (DISAGREE [talk number])”: Speaker is requesting that everyone disagree with the statement specified by [talk number]. (Ex: Everyone, please disregard talk number X)

## Interpretation of BECAUSE sentences:

“Agent2 BECAUSE (DAY  1  (Agent1 VOTE Agent2)) (vote Agent1)”: Because Agent1 voted on Agent2 (myself) on Day 1, I will vote on Agent1.

## Interpretation of INQUIRE sentences:

“Agent2 INQUIRE Agent1 (VOTED ANY)”: Agent2 wants to know who Agent1 voted against.

“Agent2 INQUIRE Agent1 (VOTE ANY)”:  Agent2 wants to know who Agent1 will vote against.

“Agent2 INQUIRE Agent1 (ESTIMATE Agent2 WEREWOLF)”: Agent2 wants to know if Agent1 considers Agent2 (itself) to be an werewolf.

## Interpretation of ANY sentences:

The ANY word is equivalent to expanding all possible substitutions, and connecting them using the OR operator. For example:

“Agent2 INQUIRE Agent1 (VOTED ANY)” is equivalent to:
“Agent2 INQUIRE Agent1 (OR (VOTED Agent1) (VOTED Agent2) (VOTED Agent3) …)

“REQUEST ANY (DIVINED [agent] [species])” is equivalent to:
OR (REQUEST Agent1 (DIVINED [agent] [species])) (REQUEST Agent2 (DIVINED [agent] [species])) ...
