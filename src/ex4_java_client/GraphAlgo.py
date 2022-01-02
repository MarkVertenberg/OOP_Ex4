import queue
from typing import List
import json
import random

from GraphAlgoInterface import GraphAlgoInterface
from Dijkstra import Dijkstra
from client_python.DiGraph import DiGraph

DIJKSTRA = Dijkstra()


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, graph=DiGraph()) -> None:
        self.graph = graph
        self.mc = 0

    def get_graph(self):
        return self.graph

    def load_from_json(self, file_name: str):
        file = file_name
        s = file[-4:]
        if s != "json":
            file_name = file_name+".json"
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
                        self.graph.add_node(t,(x, y, z))
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

    def save_to_json(self, file_name: str):
        try:
            file = open(file_name, 'w')
            file.write(json.dumps(self.savefile()))
            file.close()
            return True
        except IOError:
            return False

    def savefile(self):
        tip = []
        for e in self.graph.Lines:
            src = e[0]
            dest = e[1]
            w = self.graph.Lines[e]
            tip.append({"src": src, "w": w, "dest": dest})
        List = {}
        List["Edges"] = tip
        ver = []
        for n in self.graph.vertices.values():
            if n.dist is not None:
                r = n.value
                x = n.dist[0]
                y = n.dist[1]
                z = n.dist[2]
                pos = f'{x},{y},{z}'
                ver.append({"id": r, "pos": pos})
            else:
                ver.append({"id": n.value, "pos": None})
        List["Nodes"] = ver
        return List

    def shortest_path(self, id1: int, id2: int):
        try:
            return DIJKSTRA.shortest_path(self.graph, id1, id2)
        except ValueError as e:
            print(e)
        return float('inf'), []

    def TSP(self, node_lst: List[int]):
        sum = 0
        path = []
        if len(node_lst) > 0:
            path.append(node_lst[0])
            src = node_lst[0]
            for node in node_lst[1:]:
                algo = self.shortest_path(src, node)  # (dist, list(nodes))
                pa = algo[1]
                sum += algo[0]
                src = node
                for p in pa[1:]:
                    path.append(p)
        return path, sum

    def farthest_node_from_src(self, src):
        max = 0
        dis = 0
        for Node in self.graph.vertices:
            dis = self.shortest_path(src, Node)[0]
            if dis > max:
                max = dis
        return max

    def centerPoint(self):
        min = float("inf")
        N = None
        for Node in self.graph.vertices:
            dis = self.farthest_node_from_src(Node)
            if dis < min:
                min = dis
                N = Node
        return N, min

    def plot_graph(self):
        from GraphGUI import GraphGUI
        gui = GraphGUI(self)
        for node in self.graph.get_all_v().values():
            if not node.get_y() and not node.get_x():
                node.x = random.randint(0, gui.WIDTH)
                node.y = random.randint(0, gui.HEIGHT)
        gui.plot_graph()
