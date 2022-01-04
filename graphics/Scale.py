from OOP_Ex4.client_python.GraphInterface import GraphInterface


class Scale:

    def __init__(self, start_x=0, start_y=0, original_width=0, original_height=0, graph: GraphInterface = None, border=0):
        self.original_width = original_width
        self.original_height = original_height
        self.graph = graph
        self.start_x = start_x + border
        self.start_y = start_y + border
        self.add_border = border
        if self.graph:
            self.min_x, self.max_x, self.min_y, self.max_y = self.find_min_and_max()
            self.pixel_x, self.pixel_y = self.calculate_pixel()

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

    def calculate_pixel(self):
        pixel_x = (self.max_x - self.min_x) / (self.original_width - self.start_x - self.add_border)
        pixel_y = (self.max_y - self.min_y) / (self.original_height - self.start_y - self.add_border)
        return pixel_x, pixel_y
