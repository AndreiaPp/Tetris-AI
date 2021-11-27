import asyncio
import getpass
import json
import os
import time
import pygame
import shape

import websockets

import agent
# Next 4 lines are not needed for AI agents, please remove them from your code!
import pygame

pygame.init()
program_icon = pygame.image.load("data/icon2.png")
pygame.display.set_icon(program_icon)

original_pieces={
	"S":[[4,2],[4,3],[5,3],[5,4]], #ta
	"Z":[[4,2],[3,3],[4,3],[3,4]], #ta
	"I":[[2,2],[3,2],[4,2],[5,2]], #ta
	"O":[[3,3],[4,3],[3,4],[4,4]], #ta
 	"J":[[4,2],[5,2],[4,3],[4,4]], #ta
 	"L":[[4,2],[4,3],[4,4],[5,4]], #ta
 	"T":[[4,2],[4,3],[5,3],[4,4]] #ta
}
rotacoes = {
    "S": [[[4,2],[4,3],[5,3],[5,4]], [[4,3],[5,3],[3,4],[4,4]]],
    "Z": [[[4,2],[3,3],[4,3],[3,4]], [[3,3],[4,3],[4,4],[5,4]]],
    "I": [[[2,2],[3,2],[4,2],[5,2]], [[4,1],[4,2],[4,3],[4,4]]],
    "O": [[[3,3],[4,3],[3,4],[4,4]]],
    "J": [[[4,2],[5,2],[4,3],[4,4]], [[3,3],[4,3],[5,3],[5,4]], [[4,2],[4,3],[3,4],[4,4]], [[3,2],[3,3],[4,3],[5,3]]],
	"L": [[[4,2],[4,3],[4,4],[5,4]], [[3,3],[4,3],[5,3],[3,4]], [[3,2],[4,2],[4,3],[4,4]], [[5,2],[3,3],[4,3],[5,3]]],
    "T": [[[4,2],[4,3],[5,3],[4,4]], [[3,3],[4,3],[5,3],[4,4]], [[4,2],[3,3],[4,3],[4,4]], [[4,2],[3,3],[4,3],[5,3]]]
}


async def agent_loop(server_address="localhost:8000", agent_name="student"):
    async with websockets.connect(f"ws://{server_address}/player") as websocket:
        print("hello")
        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
        print("hello2")
        c=0
        x,y=0,0
        actions=[]
        while True:
            try:
                #print("printing the state")
                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server
                c+=1
                #print("state",state)
                if(c==1):
                    x,y=state.get('dimensions')
                    continue
                # Next lines are only for the Human Agent, the key values are nonetheless the correct ones!
                key = ""
                piece = state.get('piece')
                #print(str(len(actions))+str(piece))
                if(piece!=None):
                    if(actions==[] ):
                        actions=agent.run_ai(state.get('game'),piece,x,y)
                    else:
                        
                        key=actions.pop(0)
                    await websocket.send(
                                    json.dumps({"cmd": "key", "key": key})
                                )  # send key command to server - you must implement this send in the AI agent
                                    #break
                else:
                    actions=[]
            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return


# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))