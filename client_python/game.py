from types import SimpleNamespace
from client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *

from client_python.DiGraph import DiGraph


class game():

    def __init__(self, graph=DiGraph()):
        self.graph = graph
        self.agent = []
        self.pokemon = []

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
        for p in json_pokemons['Pokemons']:
            self.apokemon.append(pokemon(p['Pokemon']))

    def agent(self,agent_list):
         json_agent = json.loads(agent_list)
         for e in json_agent['Agents']:
          self.agent.append(Agents(e['Agent']))

    def load_from_json(self, file_name: str):
        try:
            self.graph = DiGraph()
            with open(file_name, "r") as a:
                obj = json.load(a)
                for n in obj["Nodes"]:
                    t = int(n["id"])
                    if "pos" in n:
                        m = n["pos"].split(',')
                        x = float(m[0])
                        y = float(m[1])
                        z = float(m[2])
                        self.graph.add_node(t, (x, y, z))
                    else:
                        self.graph.add_node(t)
                for e in obj["Edges"]:
                    src = int(e["src"])
                    dest = int(e["dest"])
                    w = float(e["w"])
                    self.graph.add_edge(src, dest, w)
        except IOError:
            return False
        return True

class Agents:
 def __init__(self, info: tuple):
        self.id = int(info['id'])
        self.value = float(info['value'])
        self.src = int(info['src'])
        self.dest = int(info['dest'])
        self.speed = float(info['speed'])
        pos = str(info['pos'])
        loc = pos.split(',')
        self.location = []
        for s in loc:
            self.location.append(float(s))

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

     def __init__(self, info: tuple):
         self.value = float(info['value'])
         self.type = int(info['type'])
         pos = str(info['pos'])
         loc = pos.split(',')
         self.location = []
         for s in loc:
             self.location.append(float(s))
