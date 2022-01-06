from client_python.agent import Agent
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
        print(self.graph_algo.load_from_json(self.get_graph_file_name()))
        self.client.start()
        gui = GraphGUI(self)
        while self.client.is_running() == "true":
            self.get_pokemons(self.client.get_pokemons())
            self.get_agents()
            gui.update_gui()
            self.main_algorithm()
            print(self.time_remaining(), self.client.get_info())
        self.client.stop_connection()
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
                loc4 = loc2 + loc3
                if abs(loc1 - loc4) <= lamda:
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

    def main_algorithm(self):
        for agent in self.agents:
            self.allocate(agent)
            if agent.dest == -1:
                if agent.target:
                    if agent.src == agent.target.src:
                        next_node = agent.target.dest
                    else:
                        path = DIJKSTRA.shortest_path(self.graph_algo.get_graph(), agent.src, agent.target.src)[1]
                        next_node = path[1]
                    self.client.choose_next_edge(
                        '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
        self.client.move()

    def get_score(self):
        json_grade = json.loads(self.client.get_info())
        return json_grade['GameServer']['grade']

    def get_graph_file_name(self):
        json_graph_file = json.loads(self.client.get_info())
        return "../" + json_graph_file['GameServer']['graph']

    def get_moves(self):
        json_moves = json.loads(self.client.get_info())
        return json_moves['GameServer']['moves']

    def time_remaining(self):
        return self.client.time_to_end()


game = Game()
game.run_game()
