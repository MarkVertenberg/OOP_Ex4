import pygame

from OOP_Ex4.graphics import *

WIDTH = 1080
HEIGHT = 720
GRAPH_WIDTH = 1080
GRAPH_HEIGHT = 620
REFRESH_RATE = 60


class GraphGUI:

    def __init__(self, game):
        self.game = game
        self.graph_algo = game.graph_algo
        self.screen_obj = []
        self.scalable_obj = []
        self.screen = None
        self.running = False
        self.clock = pygame.time.Clock()

    def start_gui(self, width=GRAPH_WIDTH, height=HEIGHT):
        pygame.init()
        pygame.display.set_caption("Pokemon Game")
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
        self.screen_obj = []
        for node in nodes:
            node.painter = NodePainter(node)
            self.screen_obj.append(node.painter)
        for node in nodes:
            edge_data = self.graph_algo.get_graph().all_out_edges_of_node(node.value)
            for edge in list(edge_data.keys()):
                self.screen_obj.append(EdgePainter(node.painter, self.graph_algo.get_graph().vertices[edge].painter))
        #for pokemon in self.game.pokemons:
        #    self.screen_obj.append(PokemonPainter(pokemon))
        for agent in self.game.agents:
            self.screen_obj.append(AgentPainter(agent))

    def init_scalable_objects(self):
        self.scalable_obj = []
        for node in list(self.graph_algo.get_graph().get_all_v().values()):
            node.painter = NodePainter(node)
            self.scalable_obj.append(node.painter)

    def find_border(self):
        border = 0
        for s in self.scalable_obj:
            if s.get_size() > border:
                border = s.get_size()
        return border
