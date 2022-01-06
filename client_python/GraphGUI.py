from typing import List

import pygame

from graphics import *
from graphics import Button, Text

WIDTH = 1080
HEIGHT = 720
GRAPH_WIDTH = 1080
GRAPH_HEIGHT = 620
REFRESH_RATE = 10


class GraphGUI:

    pygame.init()
    pygame.display.set_caption("Pokemon Game")
    icon = pygame.image.load('../images/pokemon_icon.png')
    pygame.display.set_icon(icon)

    def __init__(self, game):
        self.game = game
        self.graph_algo = game.graph_algo
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        menu_obj: List[ScreenObjectInterface | Scalable]
        menu_obj, self.length = self.create_objects()
        self.screen_obj = menu_obj
        self.scalable_obj = []
        self.running = True
        self.clock = pygame.time.Clock()

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
        else:
            pygame.quit()

    def draw_screen(self, width, height, outline=5):
        self.init_screen_objects()
        self.init_scalable_objects()
        scaler = Scale(0, 50, width, height, self.graph_algo.get_graph(), self.find_border() + outline)
        pygame.draw.rect(self.screen, BLACK, (0, 50, width, height - 50), outline)
        for obj in self.screen_obj:
            if type(obj).__bases__.__contains__(Scalable):
                obj.scale(scaler)
            obj.draw(self.screen)

    def init_screen_objects(self):
        nodes = list(self.graph_algo.get_graph().get_all_v().values())
        self.screen_obj = self.screen_obj[0: self.length]
        self.update_data()
        for node in nodes:
            node.painter = NodePainter(node)
            self.screen_obj.append(node.painter)
        for node in nodes:
            edge_data = self.graph_algo.get_graph().all_out_edges_of_node(node.value)
            for edge in list(edge_data.keys()):
                self.screen_obj.append(EdgePainter(node.painter, self.graph_algo.get_graph().vertices[edge].painter))
        for pokemon in self.game.pokemons:
            self.screen_obj.append(PokemonPainter(pokemon))
        for agent in self.game.agents:
            self.screen_obj.append(AgentPainter(agent))

    def init_scalable_objects(self):
        self.scalable_obj = []
        for node in list(self.graph_algo.get_graph().get_all_v().values()):
            node.painter = NodePainter(node)
            self.scalable_obj.append(node.painter)
        for pokemon in self.game.pokemons:
            self.scalable_obj.append(PokemonPainter(pokemon))
        for agent in self.game.agents:
            self.scalable_obj.append(AgentPainter(agent))

    def find_border(self):
        border = 0
        for s in self.scalable_obj:
            if s.get_size() > border:
                border = s.get_size()
        return border

    def create_objects(self):
        width, height = self.screen.get_size()[0], self.screen.get_size()[1]
        lst_obj = [Button(WHITE, width - 120, 10, 80, 30, 'STOP', text_size=36, function=self.game.client.stop),
                   Text(80, 25, 'Score: ' + str(self.game.get_score())),
                   Text(200, 25, 'Moves: ' + str(self.game.get_moves())),
                   Text(width / 2, 25, f'Time to End: {str(int(self.game.time_remaining()) / 100.0)} seconds')]
        return lst_obj, len(lst_obj)

    def update_data(self):
        width = self.screen.get_size()[0]
        self.screen_obj[0].x = width - 120
        self.screen_obj[1].text = 'Score: ' + str(self.game.get_score())
        self.screen_obj[2].text = 'Moves: ' + str(self.game.get_moves())
        self.screen_obj[3].text = f'Time to End: {str(int(self.game.time_remaining()) / 1000.0)} seconds'
        self.screen_obj[3].x = width / 2

