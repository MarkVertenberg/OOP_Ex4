import pygame

from OOP_Ex4.client_python.game import Game
from OOP_Ex4.graphics import *
from OOP_Ex4.graphics.Colors import *
from OOP_Ex4.graphics.api import Scalable

WIDTH = 1080
HEIGHT = 720
GRAPH_WIDTH = 1080
GRAPH_HEIGHT = 620
REFRESH_RATE = 60


class GraphGUI:

    def __init__(self, game: Game = None):
        self.graph_algo = game.graph_algo
        self.screen_obj = self.init_screen_objects()
        self.scalable_obj = self.init_scalable_objects()
        self.screen = None
        self.running = False
        self.clock = pygame.time.Clock()

    def start_gui(self, width=GRAPH_WIDTH, height=HEIGHT):
        pygame.init()
        pygame.display.set_caption("Graph GUI")
        icon = pygame.image.load('../graphics/images/pokemon_icon.png')
        pygame.display.set_icon(icon)
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.running = True

    def update_gui(self):
        if self.running:
            self.screen.fill(WHITE)
            if self.graph_algo:
                self.draw_screen(self.screen.get_size()[0], self.screen.get_size()[1])
                pygame.display.update()
                for event in pygame.event.get():
                    for obj in self.screen_obj:
                        obj.handle_event(event)
                    if event.type == pygame.QUIT:
                        self.running = False
            self.clock.tick(REFRESH_RATE)

    def draw_screen(self, width, height, outline=5):
        scaler = Scale(0, 50, width, height - 50, self.graph_algo.get_graph(), self.find_border())
        pygame.draw.rect(self.screen, BLACK, (0, 0, width, height), outline)
        for obj in self.screen_obj:
            if obj is Scalable:
                obj.scale(scaler)
            obj.draw(self.screen)

    def init_screen_objects(self):
        obj = []
        for node in list(self.graph_algo.get_graph().get_all_v()):
            node.painter = NodePainter(node)
            obj.append(node.painter)
        return obj

    def init_scalable_objects(self):
        obj = []
        for node in list(self.graph_algo.get_graph().get_all_v()):
            node.painter = NodePainter(node)
            obj.append(node.painter)
        return obj

    def find_border(self):
        border = 0
        for s in self.scalable_obj:
            if s.get_size() > border:
                border = s.get_size()
