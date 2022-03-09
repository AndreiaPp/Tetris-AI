# ia-tetris
Projecto de Inteligência Artificial 2021 - Tetris

## Overview
This work involves the application of concepts and techniques from three main chapters of the IA/AI course, namely: Python programming; agent architectures; and search techniques for automated problem solving.
Within the scope of this work, we developped an agent capable of playing intelligently the game Tetris, a game developed by Alexei Pajitnov in the former USSR and popularized in the early 80s of last century by Nintendo.
In Tetris, the player packs up pieces/tiles (tetrominoes) that fall vertically to fill lines. Whenever a line is completely filled it disappears and the player receives a score. The simultaneous filling of multiple lines gives the player bonus scores. The pieces that fall have a random order, but there is information about the future pieces, allowing the planning of the game in order to optimize the score. As the game evolves, the pieces fall at a higher speed, increasing the game’s difficulty. If a new piece does not fit on the game screen, it ends. The objective of the game is therefore to pack all the pieces maximizing the score.
The game’s score takes into account the number of packed pieces by the agent and the efficiency of the solutions found (privileging multiple lines in the shortest possible time).
In this repository you will find a presentation summing how our agent works along with the heuristic used.

## Authors
[Andreia Portela](https://github.com/AndreiaPp)
[Miguel Ferreira](https://github.com/MiguelF07)

## How to install

Make sure you are running Python 3.7 or higher

`$ pip install -r requirements.txt`

*Tip: you might want to create a virtualenv first*

## How to play

open 3 terminals:

`$ python3 server.py`

`$ python3 viewer.py`

`$ python3 client.py`

to play using the sample client make sure the client pygame window has focus

### Keys

Directions: arrows

## Debug Installation

Make sure pygame is properly installed:

python -m pygame.examples.aliens

# Tested on:
- OSX Big Sur 11.6

