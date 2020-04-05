AIWolf Quickstart
=================

The [AIWolf Project](http://aiwolf.org/en/introduction) aims to create an
Artificial Intelligence agent that is capable to play the Werewolf game
in place of a human player.

# What is the werewolf game?

Werewolf (Also called Mafia) is an assymetric information game.

In its simplest formulation, two teams (Werewolf Team and Villager Team) try to
eliminate all players of the opposing team. This is done through a repeated
voting process, in which all players discuss and eventually vote on a player to
be eliminated from the game.

The twist is that the Villager team has more members, who are not aware of each
other's identities, while the Werewolf team has a small number of members, who
know each other's identities. This makes the werewolf a contest of an informed
minority against an uninformed majority.

In terms of strategy, if the Villager team is able to identify the werewolf
players, they can easily use their larger numbers to vote and eliminate the
werewolfs. On the other hand, the werewolf team can use their information about
who is and who is not a werewolf to manipulate the players into voting on
players of the Villager team. In this sense, from the point of view of a
Villager player, the game is one of investigation, while from the point of view
of a Werewolf player, the game is one of deceit.

Finally, in adition of voting and elimination, the Werewolf game usually
includes Roles and special actions that can modify the game dynamic. These
abilities occur during a "night phase", which occurs after each voting stage.

Some common dynamics are: The werewolf team is able to Attack and Kill one
player during the night phase; There is a "seer" (or "cop") role in the villager
team who can discover the role of another player during the night phase; There
is a "bodyguard" (or "doctor") role in the villager team who can protect one
player from the werewolf attack during the night phase; etc.

# Roles in AIWolf

There are many variations and special roles in werewolf games. In the
AIWolf project, the game server implements the following roles:

## Villager Team Roles

* Villager: regular villager role, no special abilities.
* Seer: at each night phase, has the ability to investigate one other player
  and learn whether they are a werewolf or a villager.
* Medium: at each night phase, has the ability to investigate one player who
  was eliminated and learn whether they are a werewolf or a villager.
* Bodyguard: at each night phase, has the ability to protect one player
  (including themselves) against werewolf attacks.

## Werewolf Team Roles

* Werewolf: regular werewolf role. During the night phase, all the werewolves
  can collectively choose one player to eliminate.
* Possessed: a regular villager, but aligned with the werewolf team. The seer's
  investigation will not identify a possessed as a werewolf.

# AIWolf Competition General Rules

Following the 4th AIWolf Competition rules, there are two format of games:
5 player game, or 15 player game. The role distribution for each format is as
follows:

| Role      | 5 Players  | 15 Players |
| --------- | ----------:| ----------:|
| Villager  | 2 | 8 |
| Seer      | 1 | 1 |
| Possessed | 1 | 1 |
| Werewolf  | 1 | 3 |
| Medium    | - | 1 |
| Bodyguard | - | 1 |

The following fluxogram describes the flow of a Werewolf game in the
competition platform:

![alt text](https://github.com/ehauckdo/AIWoof/blob/master/docs/aiwolf_fluxogram.png "Fluxogram of a Werewolf game")

# Executing a Python-based agent

The official distribution of the AIWolf framework and the game server is in
Java. Therefore, the primary way of developing agents for the competition is  by
using [java files offered on the official website](http://aiwolf.org/en/server).
Basic instructions in English on which classes to inherit from are provided in
the official website.

However, since the AIWolf clients connect to the server via sockets, in
principle it should be possible to develop an agent in any language, as long
as the proper protocol is followed. For the purposes of the competitions,
as the organizers need to read and execute the code of the agents, only
a few languages are officially supported. Python is one of them.

The first Python implementation for AIWolf can be found at [Kei Harada's
repository](https://github.com/k-harada/AIWolfPy). The current repository has
the same code with minor changes.

## Setting up a server

Before running your agent, you need to set up a server.

First download the latest [server files](http://aiwolf.org/en/server) from the
website (aiwolf-ver0.5.*).

### GUI mode

The first and simplest way to execute the server is using the GUI mode. Simply
navigate to the unzipped folder and run

```
./StartServer.sh
```

This will open the GUI interface for the server. From there, you can  select the
number of players, press the "Connect" button, and the server will be ready for
agents to connect.

In addition to connecting your own agents, you can also run and connect
the sample java agents provided by the competition by using the
StartGUIClinet.sh script.

### Terminal mode

Using the GUI mode you can not automatically run a certain number of games,
which can be a problem for testing or training agents.

To get around this problem, you should use the terminal mode. First you
should edit the AutoStarter.ini file and configure the terminal mode
parameters.

```
lib=./
log=./log/			#folder to save logs
port=10000			#port to connect
game=10				#number of games to run
view=false			#show the game GUI
setting=./SampleSetting.cfg	#game related settings
agent=5 			#number of agents to play
Sample1,org.aiwolf.sample.player.SampleRoleAssignPlayer #list of java agents to connect
Sample2,org.aiwolf.sample.player.SampleRoleAssignPlayer #jar files must be on the same folder
Sample3,org.aiwolf.sample.player.SampleRoleAssignPlayer
Sample4,org.aiwolf.sample.player.SampleRoleAssignPlayer
```

If you want to connect your python-based agent, simply leave less java-based
clients in the agent list than the total number of agents specified
(alternatively, leave the agent list empty and connect only your clients). The
server is going to wait for connections until the specified number of agents is
met. After configuring the AutoStarter.ini file, you can execute the server in
terminal mode by running

```
./AutoStarter.sh
```

## Connecting the Python-based agent

To execute the python script, you need a few libraries including numpy, pandas,
etc. To check which libraries and which versions you need, check the
requirements.txt file in the root folder of this repository. You can install all
of them at once by running:

```
pip install -r requirements
```

It is highly recommended to setup a virtual environment before running this
command, to assure there will be no conflicits with libraries already installed
in your system. You can check how to install virtualenv and how to create a new
environment
[here](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/).

Once the server is set up and you have the required libraries, you can connect
the sample python agent in the current repository by executing

```
./aiwoof.py -h localhost -p 10000
```

You can also request a role to the server by passing -r [ROLE] as an argument
(roles can be VILLAGER, SEER, MEDIUM, BODYGUARD, POSSESSED, WEREWOLF).
