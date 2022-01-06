# Ex4: The Pokemon game

# Introduction:
In this project we had to realize the "Pokemon game".

![image](https://user-images.githubusercontent.com/93255163/148103741-6767c48e-07fc-445c-8319-b2eeab5fbffc.png)

- # About the game:

* The game consists of 16 stages [0-15].
* At each stage a different number of Pokemon and agents.
* The main goal at each stage is to catch as many Pokemon as possible by the agents. When the game scene actually a strongly weighted (directed) graph.
* Every Pokemon has a "weight". The same "weight" is summed up after the capture of the Pokemon.
* The goal of the game is to accumulate the maximum number of points ("score") in the smallest number of steps and in the shortest time (each game has a fixed time - usually 30-120 seconds).
* At the end of each game we will get the score and the number of steps performed.

- # Motivation:
This project is a concluding assignment of the Object Oriented Programming (OOP) course. This is an opportunity to practically experience the material being studied, to design the general algorithm then to implement the version of a working algorithm, Work as a group on "Github" , to do tests (unitest), and of course do a graphical user interface (GUI) and experiment with "Pygame".

 * **Algorithm goals:** 
 
    - The algorithm should be as efficient as possible.
    - At each stage we need to consider the number of agents and the number of Pokemon to make a pre-planning of the moves we want to make.
    - It is important to consider not only the shortest distance of the agents from these Pokemon but also the "weight" of the Pokemon, so that in the shortest time we will gain a bigger score and make fewer moves.


 * **GUI goals:** 
 
    - The GUI should be clear.
    - Should be scalable with a resizable window.
    - Should show the overall points.
    - Should show the moves counter.
    - Should show the time to end in seconds.
    - Should have a “stop” button to gracefully stop the game at any time point.


# Algorithm:

**The function below responsible for running the game:**

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

_________________________________________________________________________________________________________________________________________________________________________________
**The function below loads the Pokemons from the json files:**

    def get_pokemons(self, pokemon_list):
        json_pokemons = json.loads(pokemon_list)
        self.pokemons = []
        for p in json_pokemons['Pokemons']:
            pok = Pokemon(p['Pokemon'])
            self.find_src_dest_of_pok(pok)
            self.pokemons.append(pok)

_________________________________________________________________________________________________________________________________________________________________________________
**The function below loads the agents from the json file:**

    def get_agents(self):
        json_agent = json.loads(self.client.get_agents())
        self.agents = []
        for e in json_agent['Agents']:
            self.agents.append(Agent(e['Agent']))
            
_________________________________________________________________________________________________________________________________________________________________________________
**The function below finds the destination and source of Pokemon:**         

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

_________________________________________________________________________________________________________________________________________________________________________________
**The function below calculates the time it will take for the agent to reach Pokemon:**

    def time_from_agent_to_pok(self, agent: Agent, pok: Pokemon):
        dist = DIJKSTRA.shortest_path(self.graph_algo.get_graph(), agent.src, pok.src)[0]
        speed = agent.speed
        return dist / speed

_________________________________________________________________________________________________________________________________________________________________________________
**The function below is responsible for assigning the appropriate agent to the appropriate Pokemon:**


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

_________________________________________________________________________________________________________________________________________________________________________________
**The function below is responsible for moving the agent to the Pokemon to which it is sent:**

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

# UML:

![Untitled Diagram drawio (6)](https://user-images.githubusercontent.com/93255163/148453646-cd74b33b-83e1-4ad5-8df7-b540a600bab4.png)


# Report results:
**The results can be seen in the attached WIKI file.**  
Link: https://github.com/MarkVertenberg/OOP_Ex4/wiki/Report-results


# How to play?
**Guidance and explanation can be found on the attached WIKI file.**    
Link: https://github.com/MarkVertenberg/OOP_Ex4/wiki/How-to-play%3F


# Helpful Links:

- OXFORD COLLEGE | Directed and Edge-Weighted Graphs: 
In this site you can find information about Directed and Edge-Weighted Graphs , and the best data structure for it.   
    Link: http://math.oxford.emory.edu/site/cs171/directedAndEdgeWeightedGraphs/

- Explanation of Dijkstra’s algorithm for finding the shortest path between one vertex in a graph and another.  
This video helped us to implement our Dijkstra class.     
    Link: https://www.youtube.com/watch?v=pVfj6mxhdMw

- Explanation on performing Depth–first search (DFS) to check if A directed graph is strongly connected.   
    Link: https://www.techiedelight.com/check-given-graph-strongly-connected-not/
    
- Dijkstra's Shortest Path Algorithm - A Detailed and Visual Introduction.   
  Link: https://www.freecodecamp.org/news/dijkstras-shortest-path-algorithm-visual-introduction/
   
# Credits:
1. Mark vertenberg.
2. Mishell dubovitski.
3. Alina zakhozha.
