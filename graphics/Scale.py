from OOP_Ex4.client_python.GraphInterface import GraphInterface
from NodePainter import NodePainter


class Scale:

    def __init__(self, start_x=0, start_y=0, original_width=0, original_height=0, graph: GraphInterface = None):
        self.original_width = original_width
        self.original_height = original_height
        self.graph = graph
        self.start_x = start_x
        self.start_y = start_y
        if self.graph:
            self.min_x, self.max_x, self.min_y, self.max_y = self.find_min_and_max()
            self.pixel_x, self.pixel_y = self.__calculate_pixel()

    def scale_node(self):
        if self.pixel_x == 0:
            self.pixel_x = 0.00001
        if self.pixel_y == 0:
            self.pixel_y = 0.00001
        new_x = ((self.obj.node.get_x() - self.min_x) / self.pixel_x) + self.start_x
        new_y = ((self.obj.node.get_y() - self.min_y) / self.pixel_y) + self.start_y
        return new_x, new_y

    def find_min_and_max(self):
        if self.graph:
            max_range_x = 0.0
            min_rage_x = float('inf')
            max_range_y = 0.0
            min_rage_y = float('inf')
            nodes = list(self.graph.get_all_v().values())
            if len(nodes) > 0:
                for node in nodes:
                    if node.get_x() > max_range_x:
                        max_range_x = node.get_x()
                    if node.get_x() < min_rage_x:
                        min_rage_x = node.get_x()
                    if node.get_y() > max_range_y:
                        max_range_y = node.get_y()
                    if node.get_y() < min_rage_y:
                        min_rage_y = node.get_y()
            return min_rage_x, max_range_x, min_rage_y, max_range_y

    def __calculate_pixel(self):
        pixel_x = (self.max_x - self.min_x) / (self.original_width - self.start_x - self.obj.get_radius())
        pixel_y = (self.max_y - self.min_y) / (self.original_height - self.start_y - self.obj.get_radius())
        return pixel_x, pixel_y
