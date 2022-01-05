import pygame

from graphics import Scale
from graphics.Text import Text
from graphics.Colors import *
from client_python.DiGraph import Node
from graphics.api import *


class NodePainter(ScreenObjectInterface, Scalable):

    def __init__(self, node: Node, radius=15, outline=2, color=LIGHT_YELLOW):
        self.node = node
        self.radius = radius
        self.outline = outline
        self.color = color
        self.text = Text(node.get_x(), node.get_y(), str(self.node.get_value()))
        self.new_x = None
        self.new_y = None

    def handle_event(self, event) -> None:
        pass

    def draw(self, screen, outline=2):
        if self.new_x and self.new_y:
            self.text.x = self.new_x
            self.text.y = self.new_y
            pygame.draw.circle(screen, BLACK, (self.new_x, self.new_y), self.radius + outline)
            pygame.draw.circle(screen, self.color, (self.new_x, self.new_y), self.radius)
            self.text.draw(screen)

    def scale(self, scaler: Scale):
        pixel_x, pixel_y = scaler.calculate_pixel()
        if pixel_x == 0:
            pixel_x = 0.00001
        if pixel_y == 0:
            pixel_y = 0.00001
        self.new_x = ((self.node.get_x() - scaler.min_x) / pixel_x) + scaler.start_x
        self.new_y = ((self.node.get_y() - scaler.min_y) / pixel_y) + scaler.start_y

    def get_size(self):
        return self.radius

    def get_radius(self):
        return self.radius

