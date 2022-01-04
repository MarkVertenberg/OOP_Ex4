from os import name
from types import SimpleNamespace
from client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *
from client_python.GraphAlgo import GraphAlgo
from client_python.DiGraph import DiGraph
import graphics


# init pygame
WIDTH, HEIGHT = 1080, 720

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'

client = Client()


class Game():
    def __init__(self, GraphAlgo=GraphAlgo):
        self.Graphalgo = GraphAlgo
        self.agents = self.agent
        self.pokemons = []
        self.unit = []
        self.free = []
        
    def run_game():
        pygame.init()
        screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
        clock = pygame.time.Clock()
        pygame.font.init()
        

    def free_agents(self):
         visited = [False] * len(self.agents)
         for agent in self.agents:
             

    def allocate_pokemon(self): 
        list = {}
        i = 0
        for agent in self.agents:
            list.pop(agent,pokemon[i])
        i = i+1    
             
        pass




    """
    pokemons = json.loads(client.get_pokemons(),
                          object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    pokemons = [p.Pokemon for p in pokemons]
    for p in pokemons:
        x, y, _ = p.pos.split(',')
        p.pos = SimpleNamespace(x=my_scale(float(x), x=True), y=my_scale(float(y), y=True))
    agents = json.loads(client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [agent.Agent for agent in agents]
    for a in agents:
        x, y, _ = a.pos.split(',')
        a.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
            """
    def pokemon(self, pokemon_list):
        json_pokemons = json.loads(pokemon_list)
        self.pokemons = []
        for p in json_pokemons['Pokemons']:
            self.pokemons.append(pokemon(p['Pokemon']))

    def agent(self,agent_list):
        json_agent = json.loads(agent_list)
        self.agents = []
        for e in json_agent['Agents']:
            self.agents.append(Agents(e['Agent']))


class Agents:
    """
    "Agent":
    {
        "id":0,
        "value":0.0,
        "src":0,
        "dest":1,
        "speed":1.0,
        "pos":"35.18753053591606,32.10378225882353,0.0"
    }
    """
    def __init__(self, info: dict):
        self.id = int(info['id'])
        self.value = float(info['value'])
        self.src = int(info['src'])
        self.dest = int(info['dest'])
        self.speed = float(info['speed'])
        pos = str(info['pos'])
        loc = pos.split(',')
        self.location = (loc[0], loc[1])

    def id(self):
        return self.id    


class pokemon:
    """
    "Pokemons": [
    {
        "Pokemon": {
            "value": 5.0,
            "type": -1,
            "pos": "35.197656770719604,32.10191878639921,0.0"
        }
    """

    def __init__(self, info: dict):
        self.value = float(info['value'])
        self.type = int(info['type'])
        pos = str(info['pos'])
        loc = pos.split(',')
        self.location = (loc[0], loc[1])
        self.src = self.src_node()
        self.dest = self.dest_node()
    
    def src_node(self):
        pass

    def dest_node(self):
        pass

if __name__ == 'main':
    client.start_connection(HOST, PORT)
    graph_algo = GraphAlgo()
    graph_algo.load_from_json(client.get_graph())
    game = Game(graph_algo)
    game.run_game()
    