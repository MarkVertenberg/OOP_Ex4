import math
import pygame

from Text import Text
from Scale import Scale
from Colors import *
from OOP_Ex4.client_python.DiGraph import Node
from api import *

SCALER = Scale()


class NodePainter(ScreenObjectInterface):

    def __init__(self, node: Node, radius=15, outline=2, color=LIGHT_YELLOW):
        self.node = node
        self.out_edges = []
        self.radius = radius
        self.outline = outline
        self.color = color
        self.text = Text(node.get_x(), node.get_y(), str(self.node.get_value()))
        self.over = False
        self.new_x = None
        self.new_y = None

    def draw(self, screen, outline=2):
        SCALER.__init__(start_x + outline, start_y + outline, original_width - outline, original_height - outline, graph, self)
        self.new_x, self.new_y = SCALER.scale_node()
        self.text.x = self.new_x
        self.text.y = self.new_y
        pygame.draw.circle(screen, BLACK, (self.new_x, self.new_y), self.radius + outline)
        if self.over:
            pygame.draw.circle(screen, WHITE, (self.new_x, self.new_y), self.radius)
            self.text.text = "(" + str(self.node.get_x()) + "," + str(self.node.get_y()) + ")"
        else:
            pygame.draw.circle(screen, self.color, (self.new_x, self.new_y), self.radius)
            self.text.text = str(self.node.get_value())
        self.text.draw(screen, )

        self.update_edges(graph)
        for edge in self.out_edges:
            edge.draw(screen, )

    def get_radius(self):
        return self.radius

    def update_edges(self, graph):
        from EdgePainter import EdgePainter
        self.out_edges = []
        if self.node:
            for dest in list(self.node.outWard.keys()):
                self.out_edges.append(EdgePainter(self, graph.get_all_v().get(dest).painter, self.node.outWard.get(dest), self.color))
