import math
from client import Client
import json
import pygame
from pygame import *
from client_python.GraphAlgo import GraphAlgo
from client_python.DiGraph import Node
from client_python.game import Agents
from client_python.Dijkstra import Dijkstra
lamda = 0.001

DIJKSTRA = Dijkstra()
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
        self.pokemons = {}
        self.unit = []
        self.agents = {}


    def run_game(self):
        pygame.init()
        screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
        clock = pygame.time.Clock()
        pygame.font.init()

    def pokemon(self, pokemon_list):
        json_pokemons = json.loads(pokemon_list)
        self.pokemons = []
        for p in json_pokemons['Pokemons']:
            self.pokemons.append(pokemon(p['Pokemon']))

    def agent(self, agent_list):
        json_agent = json.loads(agent_list)
        self.agents = []
        for e in json_agent['Agents']:
            self.agents.append(Agents(e['Agent']))

    def find_src_dest_of_pok(self, pok: pokemon):
        for ver1 in self.Graphalgo.get_graph():
            for ver2 in self.Graphalgo.get_graph():
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

    def time_from_agent_to_pok(self, agent: Agents, pok: pokemon):
        dist = DIJKSTRA.shortest_path(self.Graphalgo.get_graph(), agent.src, pok.src)[0]
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

    def find_best_pokemon(self, a: Agents):
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




class Agents:
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


class pokemon:
    def __init__(self, info: dict):
        self.value = float(info['value'])
        self.type = int(info['type'])
        pos = str(info['pos'])
        loc = pos.split(',')
        self.location = (loc[0], loc[1])
        self.x = loc[0]
        self.y = loc[1]
        self.src = 0
        self.dest = 0
        self.agent = None

    def dist_pok_from_ver(self, ver: Node):
        x_v = pow((self.location[0] - ver.x), 2)
        y_v = pow(self.location[1] - ver.y, 2)
        dist = math.sqrt(x_v + y_v)
        return dist

    def src_node(self):
        return self.src

    def dest_node(self):
        return self.dest

if __name__ == 'main':
    client.start_connection(HOST, PORT)
    graph_algo = GraphAlgo()
    graph_algo.load_from_json(client.get_graph())
    game = Game(graph_algo)
    game.run_game()
    