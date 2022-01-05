import math

from OOP_Ex4.client_python.DiGraph import Node


class Pokemon:
    def __init__(self, info: dict):
        self.value = float(info['value'])
        self.type = int(info['type'])
        pos = str(info['pos'])
        loc = pos.split(',')
        self.x = float(loc[0])
        self.y = float(loc[1])
        self.src = self.src_node()
        self.dest = self.dest_node()
        self.agent = None

    def dist_pok_from_ver(self, ver: Node):
        x_v = pow(self.x - ver.x, 2)
        y_v = pow(self.y - ver.y, 2)
        dist = math.sqrt(x_v + y_v)
        return dist

    def src_node(self):
        return None

    def dest_node(self):
        return None