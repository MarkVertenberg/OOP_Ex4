import math

from client_python.agent import Agent
from client_python.DiGraph import Node
from client_python.GraphAlgo import GraphAlgo
from client_python.pokemon import Pokemon
from client_python.client import Client
from client_python.GraphGUI import GraphGUI
import json
from client_python.Dijkstra import Dijkstra

lamda = 0.000000000001

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
            self.get_pokemons(self.client.get_pokemons())
            self.get_agents()
            gui.update_gui()
            self.main_algorithm()
        exit(0)

    def get_pokemons(self, pokemon_list):
        json_pokemons = json.loads(pokemon_list)
        self.pokemons = []
        for p in json_pokemons['Pokemons']:
            pok = Pokemon(p['Pokemon'])
            self.find_src_dest_of_pok(pok)
            self.pokemons.append(pok)

    def get_agents(self):
        json_agent = json.loads(self.client.get_agents())
        self.agents = []
        for e in json_agent['Agents']:
            self.agents.append(Agent(e['Agent']))

    def find_src_dest_of_pok(self, pok: Pokemon):
        for ver1 in list(self.graph_algo.get_graph().get_all_v().values()):
            for ver2 in list(self.graph_algo.get_graph().get_all_v().values()):
                loc1 = ver1.distance(ver2)
                loc2 = pok.dist_pok_from_ver(ver1)
                loc3 = pok.dist_pok_from_ver(ver2)
                loc4 = loc2+loc3
                if abs(loc1-loc4) <= lamda:
                    if pok.type == -1:
                        pok.src = max(ver1.value, ver2.value)
                        pok.dest = min(ver1.value, ver2.value)
                    else:
                        pok.src = min(ver1.value, ver2.value)
                        pok.dest = max(ver1.value, ver2.value)
                    return

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
            for j in range(0, len(self.pokemons) - list.index(p) - 1):
                value1 = list[j].value
                value2 = list[j + 1].value
                if value1 > value2:
                    temp = list[j]
                    list[j] = list[j + 1]
                    list[j + 1] = temp
        return list

    def sort_dist_from_pok(self, agent: Agent):
        list = []
        for p in self.sort_pokemon():
            list.append(p)

        for p in list:
            for j in range(0, len(self.sort_pokemon()) - list.index(p) - 1):
                time1 = self.time_from_agent_to_pok(agent, list[j])
                time2 = self.time_from_agent_to_pok(agent, list[j + 1])
                if time1 < time2:
                    temp = list[j]
                    list[j] = list[j + 1]
                    list[j + 1] = temp
        return list

    # returns list with points for pokimons, when the index is bigger so is the points
    def points_for_best(self, agent: Agent):
        point_list = {}
        for dis in self.sort_dist_from_pok(agent):
            for pok in self.sort_pokemon():
                if dis == pok:
                    points = self.sort_dist_from_pok(agent).index(dis) + self.sort_pokemon().index(pok)
                    point_list[points] = pok
        l = list(point_list.keys())
        l.sort()
        l2 = []
        for i in l:
            l2.append(point_list.get(i))
        return l2

    def allocate(self, a: Agent):
        min_time = float('inf')
        close_pok = None
        for pok in self.pokemons:
            if pok.waiting_for is None:
                time = self.time_from_agent_to_pok(a, pok)
                if time < min_time:
                    close_pok = pok
                    min_time = time
        if close_pok:
            a.target = close_pok
            close_pok.waiting_for = a

    def is_collected(self, a: Agent):
        if a.src is not None and a.target is not None:
            if a.src == a.target.dest:
                a.target = None

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
        for agent in self.agents:
            if agent.dest == -1:
                self.is_collected(agent)
                self.allocate(agent)
                if agent.target:
                    if agent.src == agent.target.src:
                        print(agent.target.dest)
                        next_node = agent.target.dest
                    else:
                        print('pass2')
                        path = DIJKSTRA.shortest_path(self.graph_algo.get_graph(), agent.src, agent.target.src)[1]
                        next_node = path[1]
                    self.client.choose_next_edge('{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
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
    