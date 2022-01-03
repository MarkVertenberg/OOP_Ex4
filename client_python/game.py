
import json

from client_python.GraphAlgo import GraphAlgo
from client_python.DiGraph import DiGraph

class game():
    def __init__(self, GraphAlgo=GraphAlgo, graph=DiGraph):
        self.Graphalgo = GraphAlgo
        self.graph = graph
        self.agent = []
        self.pokemon = []

    def pokemon(self, pokemon_list):
        json_pokemons = json.loads(pokemon_list)
        for p in json_pokemons['Pokemons']:
            self.pokemon.append(pokemon(p['Pokemon']))

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
 def __init__(self, info: dict):
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

class pokemon:
 def __init__(self, info: dict):
         self.value = float(info['value'])
         self.type = int(info['type'])
         pos = str(info['pos'])
         loc = pos.split(',')
         self.location = []
         for s in loc:
             self.location.append(float(s))
