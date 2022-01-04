from typing import List

import pygame

from OOP_Ex4.client_python.game import game
from OOP_Ex4.graphics import *
from GraphInterface import GraphInterface

WIDTH = 1280
HEIGHT = 720
GRAPH_WIDTH = 960
GRAPH_HEIGHT = 720
REFRESH_RATE = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
SKY_BLUE = (75, 118, 229)
LIGHT_YELLOW = (255, 253, 126)


class GraphGUI:

    WIDTH = WIDTH
    HEIGHT = HEIGHT
    GRAPH_WIDTH = GRAPH_WIDTH

    def __init__(self, game_obj: game = None):
        self.graph_algo = game_obj.graph_algo
        self.nodes = None
        self.screen = None
        self.running = True
        self.clock = pygame.time.Clock()

    def run_gui(self, width=GRAPH_WIDTH, height=HEIGHT):
        pygame.init()
        pygame.display.set_caption("Graph GUI")
        icon = pygame.image.load('../graphics/images/pokemon_icon.png')
        pygame.display.set_icon(icon)
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        while self.running:
            self.screen.fill(WHITE)
            if self.graph_algo:
                nodes = list(self.graph_algo.get_graph().get_all_v().values())
                self.show_graph(self.screen.get_size()[0], self.screen.get_size()[1], self.graph_algo.get_graph())
                pygame.display.update()
                for event in pygame.event.get():
                    for node in nodes:
                        node.painter.handle_event(event)
                    if event.type == pygame.QUIT:
                        self.running = False
            self.clock.tick(REFRESH_RATE)
        pygame.quit()

    def show_graph(self, width, height, graph: GraphInterface, outline=5):
        pygame.draw.rect(self.screen, BLACK, (0, 0, width, height), outline)
        if graph:
            nodes = graph.get_all_v().values()
            for node in nodes:
                node.painter.draw(self.screen, )

    def show_buttons(self, buttons: List[Button]):
        for button in buttons:
            button.draw(self.screen, 2)
