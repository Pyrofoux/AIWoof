# [💀] Killer Queen


*«I'm going to eliminate you now, before you have a chance to speak, so I can sleep soundly again tonight.» - Yoshikage Kira*

<p align="center">
  <img width="200px" src="docs/KQ-stand.png">
</p>


**Killer Queen** is an agent participating in the International [AIWolf](http://aiwolf.org/en/introduction) Competition. The goal is to make bots play the [Werewolf](https://werewolf.chat/) game together!

This repository contains the source code of Killer Queen, as well as the necessary files to run simulations and documentation on how to setup your own agent.

For any questions or suggestions, contact me at [yrabii@ensc.fr](mailto:yrabii@ensc.fr), or on [Twitter](twitter.com/Pyrofoux).

# What is AIWolf?

*Parts of this repository were adapted from [`ehauckdo/AIWoof`](https://github.com/ehauckdo/AIWoof)*

**AIWolf** is a project dedicated to creating virtual agents capable of playing the Werewolf game. To understand why this problem is important, please check this [presentation](http://aiwolf.org/en/introduction) of the project. In the AIWolf Competition, participants must create AI agents and make them compete with each other.

To learn the rules and how to play the Werewolf game, please refer to [this
website](https://werewolf.chat/Main_Page)

The AI Competition currently has 2 branches, one protocol-based where agents can
use a predefined grammar to communicate, and one NLP-based. This repository has
information on the protocol-based branch of the competition.

See the [Manual folder/](docs/manual/) for information about how to setup your own agents :
- [Quick Start](docs/manual/QuickStart.md) to understand the course of the game
- [Protocol](docs/manual/Protocol.md) for details about the communication protocol between agents
- [Agent Programming](docs/manual/AgentProgramming.md) for documentations about the functions your agent should use

# Contents of this repo

- [/server](server) : the AIWolf server that run Werewolf games with several agents
- [/killerQueen](killerQueen) : code source of the Killer Queen agent
- [/other_agents](other_agents) : code source of other public agents, for testing purpose
- [/archive](archive) : older versions of Killer Queen

# How to run a test game

1. Configure the game's settings in `gameSettings.ini`. follow the format specified to choose games composition (agents algorithms and roles). Here are useful parameters:
  - `game` (int) : number of games to simulate

  - `log` (path) : path to the folder where the server will write game logs

  - `view` (bool) : use the GUI to follow the course of the game (Japanese)


2. Start the server.
* Windows : launch [RUN.bat](RUN.bat) or [server/AutoStarter.bat](server/AutoStarter.bat)
* Linux : launch [RUN.sh](RUN.sh) or [server/AutoStarter.bat](server/AutoStarter.bat)
