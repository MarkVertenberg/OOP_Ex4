import math

from OOP_Ex4.client_python.agent import Agent
from OOP_Ex4.client_python.DiGraph import Node
from OOP_Ex4.client_python.GraphAlgo import GraphAlgo
from OOP_Ex4.client_python.pokemon import Pokemon
from OOP_Ex4.client_python.client import Client
from OOP_Ex4.client_python.GraphGUI import GraphGUI
import json
from OOP_Ex4.client_python.Dijkstra import Dijkstra
lamda = 0.001

DIJKSTRA = Dijkstra()
# init pygame
WIDTH, HEIGHT = 1080, 720


# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'


class Game:

    def __init__(self):
        self.client = Client()
        self.graph_algo = GraphAlgo()
        self.agents = []
        self.pokemons = []
        self.unit = []
        self.agents = {}

    def run_game(self):
        self.client.start_connection(HOST, PORT)
        self.client.add_agent("{\"id\":0}")
        self.client.add_agent("{\"id\":1}")
        self.client.add_agent("{\"id\":2}")
        self.client.add_agent("{\"id\":3}")
        file_location = '../data/graph_file_json'
        with open(file_location, 'w') as f:
            f.write(self.client.get_graph())
        self.graph_algo.load_from_json(file_location)
        self.client.start()
        gui = GraphGUI(self)
        gui.start_gui()
        while self.client.is_running() == "true":
            self.pokemon(self.client.get_pokemons())
            self.agent(self.client.get_agents())
            gui.update_gui()
            self.client.move()
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
        for ver1 in list(self.graph_algo.get_graph().get_all_v().values()):
            for ver2 in list(self.graph_algo.get_graph().get_all_v().values()):
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

        # biggest value in first place in array

    def sort_pokemon(self):
        list = []
        for p in self.pokemons:
            list.append(p)
        for p in list:
            for j in range(0, len(self.pokemons) - p - 1):
                value1 = list[j].value
                value2 = list[j + 1].value
                if value1 > value2:
                    list[j], list[j + 1] = list[j + 1], list[j]
        return list

    def sort_dist_from_pok(self, agent: Agent):
        list = []
        for p in self.sort_pokemon():
            list.append(p)

        for p in list:
            for j in range(0, len(self.sort_pokemon()) - p - 1):
                time1 = self.time_from_agent_to_pok(agent, list[j])
                time2 = self.time_from_agent_to_pok(agent, list[j + 1])
                if time1 < time2:
                    list[j], list[j + 1] = list[j + 1], list[j]

        return list

        # returns list with points for pokimons, when the index is bigger so is the points

    def points_for_best(self, agent: Agent):
        point_list = []
        for dis in self.sort_dist_from_pok(agent):
            for pok in self.sort_pokemon():
                if dis == pok:
                    points = self.sort_dist_from_pok(agent).index(dis) + self.sort_pokemon().index(pok)
                    point_list[points] = pok

        return point_list

    def allocate(self, a: Agent):
        length = len(self.points_for_best(a))
        a.pokemon = self.points_for_best(a)[length - 1]

        return a.pokemon.src

    """ def find_best_agent(self, pok: Pokemon):
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
           for p in self.pokemons:
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
       """

    """def allo(self):
        visited = [False] * len(self.agents)
        min = float('inf')
        a = None
        pok = None
        for agent in self.agents:
           if visited[agent]:
            for p in self.sort_pokemon():
             time = self.time_from_agent_to_pok(agent, p)
             if time < min:
                 min = time
                 a = agent
                 pok = p
                 visited[agent] = False

        pok.a
        a.pok
        """
    def main_algorithm(self):
        for agent in self.agents.values():
            if agent.dest == -1:
                path = DIJKSTRA.shortest_path(agent.src, self.allocate(agent))[1]
                next_node = path[1]
                self.client.choose_next_edge(
                    '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
                ttl = self.client.time_to_end()
                print(ttl, self.client.get_info())

        self.client.move()

    def get_score(self):
        json_grade = json.loads(self.client.get_info())
        return json_grade['GameServer']['grade']

    def time_remaining(self):
        return self.client.time_to_end()


game = Game()
game.run_game()
    