import math

from OOP_Ex4.client_python.DiGraph import Node
from OOP_Ex4.client_python.GraphAlgo import GraphAlgo
from OOP_Ex4.client_python.GraphGUI import GraphGUI
from OOP_Ex4.client_python.client import Client

from client import Client
import json
import pygame
from OOP_Ex4.client_python.Dijkstra import Dijkstra
lamda = 0.001

DIJKSTRA = Dijkstra()
# init pygame
WIDTH, HEIGHT = 1080, 720


# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'

client = Client()


class Agent:
    def __init__(self, info: dict):
        self.id = int(info['id'])
        self.value = float(info['value'])
        self.src = int(info['src'])
        self.dest = int(info['dest'])
        self.speed = float(info['speed'])
        pos = str(info['pos'])
        loc = pos.split(',')
        self.location = (loc[0], loc[1])
        self.pokemon = None

    def id(self):
        return self.id


class Pokemon:
    def __init__(self, info: dict):
        self.value = float(info['value'])
        self.type = int(info['type'])
        pos = str(info['pos'])
        loc = pos.split(',')
        self.location = (loc[0], loc[1])
        self.x = loc[0]
        self.y = loc[1]
        self.src = self.src_node()
        self.dest = self.dest_node()
        self.agent = None

    def dist_pok_from_ver(self, ver: Node):
        x_v = pow(float(self.location[0]) - ver.x, 2)
        y_v = pow(float(self.location[1]) - ver.y, 2)
        dist = math.sqrt(x_v + y_v)
        return dist

    def src_node(self):
        return self.src

    def dest_node(self):
        return self.dest


class Game:
    def __init__(self, algo):
        self.graph_algo = algo
        self.agents = self.agent
        self.pokemons = {}
        self.unit = []
        self.agents = {}

    def run_game(self):
        client.add_agent("{\"id\":0}")
        client.add_agent("{\"id\":1}")
        client.add_agent("{\"id\":2}")
        client.add_agent("{\"id\":3}")
        client.start()
        gui = GraphGUI(self)
        gui.start_gui()
        while client.is_running() == "true":
            gui.update_gui()
            client.move()
        exit(0)

    def pokemon(self, pokemon_list):
        json_pokemons = json.loads(pokemon_list)
        self.pokemons = []
        for p in json_pokemons['Pokemons']:
            self.pokemons.append(Pokemon(p['Pokemon']))

    def agent(self, agent_list):
        json_agent = json.loads(agent_list)
        self.agents = []
        for e in json_agent['Agents']:
            self.agents.append(Agent(e['Agent']))

    def find_src_dest_of_pok(self, pok: pokemon):
        for ver1 in self.graph_algo.get_graph():
            for ver2 in self.graph_algo.get_graph():
             loc1 = self.dist_of_2_ver(ver1, ver2)
             loc2 = pok.dist_pok_from_ver(ver1)
             loc3 = pok.dist_pok_from_ver(ver2)
             loc4 = loc2+loc3
             if abs(loc1-loc4) <= lamda:
                 pok.src = min(ver1.x, ver2.y)
                 pok.dest = max(ver1.y, ver2.y)

    def dist_of_2_ver(self,ver1: Node, ver2: Node):
        x_v = pow((ver1.x - ver2.x), 2)
        y_v = pow(ver1.y - ver2.y, 2)
        dist = math.sqrt(x_v + y_v)
        return dist

    def list_of_agents(self):
        list = []
        for agent in self.agents.values():
            list.append(agent.id)
        return list

        # the time for agent to get to to pokemon

    def time_from_agent_to_pok(self, agent: Agent, pok: Pokemon):
        dist = DIJKSTRA.shortest_path(self.graph_algo.get_graph(), agent.src, pok.src)[0]
        speed = agent.speed
        return dist / speed

    def find_best_agent(self, pok: pokemon):
        min = float('inf')
        a = None
        list = self.list_of_agents()
        for agent in list:
            val = self.time_from_agent_to_pok(agent, pok)
            if val < min:
                min = val
                a = agent
        pok.agent = a

    def find_best_pokemon(self, a: Agent):
        max = 0
        pok = None
        for p in self.pokemons.values():
            if p.value > max:
                max = p.value
                pok = p

        a.pokemon = pok

    def allocate(self):
       for p in self.pokemons:
           if p.agent is None:
               self.find_best_agent(p)
       for a in self.agents:
           if a.pokemon is None:
               self.find_best_pokemon(a)

    def client(self, client: client):
        for agent in self.agents.values():
            if agent.dest == -1:
                next_node = (agent.src - 1) % len(GraphAlgo.get_graph().Nodes)
                client.choose_next_edge(
                    '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
                ttl = client.time_to_end()
                print(ttl, client.get_info())

        client.move()


client.start_connection(HOST, PORT)
graph_algo = GraphAlgo()
file_location = '../data/graph_file_json'
with open(file_location, 'w') as f:
    f.write(client.get_graph())
print(graph_algo.load_from_json(file_location))
game = Game(graph_algo)
game.run_game()
    