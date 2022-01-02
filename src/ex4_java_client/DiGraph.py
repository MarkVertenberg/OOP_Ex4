import math


from GraphInterface import GraphInterface


class DiGraph(GraphInterface):

    def __init__(self):
        self.vertices = {}
        self.Lines = {}
        self.mc = 0

    def __repr__(self) -> str:
        return f'Graph: |V|= {self.v_size()}, |E|= {self.e_size()}'

    def v_size(self):
        return len(self.vertices)

    def e_size(self):
        return len(self.Lines)

    def get_all_v(self):
        return self.vertices

    def all_in_edges_of_node(self, id1: int):
        if self.vertices.get(id1) is not None:
            return self.vertices[id1].inWard
        return {}

    def all_out_edges_of_node(self, id1: int):
        if self.vertices.get(id1) is not None:
            return self.vertices[id1].outWard
        return {}

    def get_mc(self):
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float):
        if id1 not in self.vertices or id2 not in self.vertices:
            return False
        if self.Lines.get((id1, id2)) is None:
            self.Lines[(id1, id2)] = weight
            self.vertices[id1].outWard[id2] = weight
            self.vertices[id2].inWard[id1] = weight
            self.mc = self.mc + 1
            return True
        return False

    def add_node(self, node_id: int, pos: tuple = None):
        if self.vertices.get(node_id) is None:
            self.vertices[node_id] = Node(node_id, pos)
            self.mc = self.mc + 1
            return True
        return False

    def remove_node(self, node_id: int):
        if self.vertices[node_id] is not None:
            to_remove = []
            for from_out in self.vertices[node_id].inWard:
                to_remove.append((from_out, node_id))
            for to_dest in self.vertices[node_id].outWard:
                to_remove.append((node_id, to_dest))
            for edge in to_remove:
                self.remove_edge(edge[0], edge[1])
            self.vertices.pop(node_id)
            self.mc = self.mc + 1
            return True
        return False

    def remove_edge(self, node_id1: int, node_id2: int):
        if self.vertices.get(node_id1) is not None and self.vertices.get(node_id2) is not None:
            if self.vertices[node_id2].inWard.get(node_id1) and self.vertices[node_id1].outWard.get(node_id2):
                self.vertices[node_id1].outWard.pop(node_id2)
                self.vertices[node_id2].inWard.pop(node_id1)
                self.Lines.pop((node_id1, node_id2))
                self.mc += 1
                return True
        return False


class Node:
    def __init__(self, value, dist: tuple = None):
        from src.graphics.NodePainter import NodePainter
        self.value = value
        self.outWard = {}
        self.inWard = {}
        self.dist = dist
        self.x = None
        self.y = None
        if dist:
            self.x = dist[0]
            self.y = dist[1]
        self.painter = NodePainter(self)

    def __repr__(self) -> str:
        return f'{self.value}: |edges_out| {len(self.outWard)} |edges_in| {len(self.inWard)}'

    def get_value(self):
        return self.value

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def distance(self, other):
        x = math.pow((other.get_x() - self.x), 2)
        y = math.pow((other.get_y() - self.y), 2)
        return math.sqrt(x + y)
