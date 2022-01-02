import math

import pygame

from src.DiGraph import Node
from src.graphics.Text import Text

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
SKY_BLUE = (75, 118, 229)
LIGHT_YELLOW = (255, 253, 126)


class NodePainter:

    def __init__(self, node: Node, radius=15, outline=2, color=LIGHT_YELLOW):
        from src.graphics.Scale import Scale
        self.node = node
        self.out_edges = []
        self.radius = radius
        self.outline = outline
        self.color = color
        self.text = Text(node.get_x(), node.get_y(), str(self.node.get_value()))
        self.over = False
        self.scaler = Scale()
        self.new_x = None
        self.new_y = None
        self.dest = None

    def handle_event(self, event):
        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEMOTION:
            if self.is_over(pos):
                self.over = True
            else:
                self.over = False

    def draw(self, screen, start_x, start_y, original_width, original_height, graph, outline=2):
        self.scaler.__init__(start_x + outline, start_y + outline, original_width - outline, original_height - outline,
                             graph, self)
        self.new_x, self.new_y = self.scaler.scale_node()
        self.text.x = self.new_x
        self.text.y = self.new_y
        pygame.draw.circle(screen, BLACK, (self.new_x, self.new_y), self.radius + outline)
        if self.over:
            pygame.draw.circle(screen, WHITE, (self.new_x, self.new_y), self.radius)
            self.text.text = "(" + str(self.node.get_x()) + "," + str(self.node.get_y()) + ")"
        else:
            pygame.draw.circle(screen, self.color, (self.new_x, self.new_y), self.radius)
            self.text.text = str(self.node.get_value())
        self.text.draw(screen)

        self.update_edges(graph)
        for edge in self.out_edges:
            edge.draw(screen)
        if self.dest is not None:
            for edge in self.out_edges:
                if edge.dest.node.value == self.dest:
                    edge.draw(screen, 4)

    def set_radius(self, radius):
        pass

    def get_radius(self):
        return self.radius

    def is_over(self, pos):
        a = pos[0] - self.node.get_x()
        b = pos[1] - self.node.get_y()
        if self.new_x and self.new_y:
            a = pos[0] - self.new_x
            b = pos[1] - self.new_y
        return math.pow(a, 2) + math.pow(b, 2) <= math.pow(self.radius, 2)

    def update_edges(self, graph):
        from src.graphics.EdgePainter import EdgePainter
        self.out_edges = []
        if self.node:
            for dest in list(self.node.outWard.keys()):
                color = BLACK
                if self.dest and self.dest == dest:
                    color = GREEN
                self.out_edges.append(EdgePainter(self, graph.get_all_v().get(dest).painter, self.node.outWard.get(dest), color))
