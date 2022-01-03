from typing import List

import pygame

from client_python.graphics.Button import Button
from client_python.graphics.InputBox import InputBox
from client_python.graphics.LittleWindow import LittleWindow
from graphics import *
from GraphAlgo import GraphAlgo
from GraphAlgoInterface import GraphAlgoInterface
from GraphInterface import GraphInterface
from client_python.graphics.NodePainter import NodePainter

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

    def __init__(self, graph_algo: GraphAlgoInterface = None):
        self.graph_algo = graph_algo
        self.nodes = None
        self.screen = None
        self.running = True
        self.clock = pygame.time.Clock()

    def run_gui(self):
        pygame.init()
        pygame.display.set_caption("Graph GUI")
        icon = pygame.image.load('graphics/images/graph_icon.jpg')
        pygame.display.set_icon(icon)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        if self.graph_algo:
            self.main_screen()
        else:
            self.graph_algo = GraphAlgo()
            self.main_screen()

    def plot_graph(self, width=GRAPH_WIDTH, height=HEIGHT):
        pygame.init()
        pygame.display.set_caption("Graph GUI")
        icon = pygame.image.load('graphics/images/graph_icon.jpg')
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

    def main_screen(self):
        list_buttons = self.create_buttons()
        while self.running:
            self.screen.fill(WHITE)
            self.show_graph(WIDTH * 0.75, HEIGHT, self.graph_algo.get_graph())
            self.show_buttons(list_buttons)
            pygame.display.update()
            for event in pygame.event.get():
                nodes = list(self.graph_algo.get_graph().get_all_v().values())
                for node in nodes:
                    node.painter.handle_event(event)
                for button in list_buttons:
                    button.handle_event(event)
                if event.type == pygame.QUIT:
                    self.running = False
            self.clock.tick(REFRESH_RATE)
        pygame.quit()

    def show_graph(self, width, height, graph: GraphInterface, outline=5):
        pygame.draw.rect(self.screen, BLACK, (0, 0, width, height), outline)
        if graph:
            nodes = graph.get_all_v().values()
            for node in nodes:
                node.painter.draw(self.screen, outline, outline, width - outline, height - outline, graph)

    def show_buttons(self, buttons: List[Button]):
        for button in buttons:
            button.draw(self.screen, 2)

    def create_buttons(self):

        load_graph_input_box = InputBox(10, 10, 200, 30, "Path", text_size=16)
        load = Button(WHITE, 220, 10, 80, 30, "Load", text_size=16)
        load_window = LittleWindow([load_graph_input_box], load, function="load_from_json", graph_algo=self.graph_algo)
        load_button = Button(WHITE, WIDTH * 0.75, 0, WIDTH * 0.25, HEIGHT * (1 / 9.0), "Load Graph", window=load_window)

        save_graph_input_box = InputBox(10, 10, 200, 30, "Path", text_size=16)
        save = Button(WHITE, 220, 10, 80, 30, "Save", text_size=16)
        save_window = LittleWindow([save_graph_input_box], save, function="save_to_json", graph_algo=self.graph_algo)
        save_button = Button(WHITE, WIDTH * 0.75, HEIGHT * (1 / 9.0), WIDTH * 0.25, HEIGHT * (1 / 9.0), "Save Graph", window=save_window)

        id_input_box = InputBox(10, 10, 65, 30, "Id", text_size=16)
        x_add_node_input_box = InputBox(80, 10, 65, 30, "X", text_size=16)
        y_add_node_input_box = InputBox(150, 10, 65, 30, "Y", text_size=16)
        add_node = Button(WHITE, 220, 10, 80, 30, "Add", text_size=16)
        add_node_window = LittleWindow([id_input_box, x_add_node_input_box, y_add_node_input_box], add_node, function="add_node", graph_algo=self.graph_algo)
        add_node_button = Button(WHITE, WIDTH * 0.75, (HEIGHT * (1 / 9.0)) * 2, WIDTH * 0.25, HEIGHT * (1 / 9.0), "Add Node", window=add_node_window)

        remove_node_input_box = InputBox(10, 10, 200, 30, "Node Id", text_size=16)
        remove_node = Button(WHITE, 220, 10, 80, 30, "Remove", text_size=16)
        remove_node_window = LittleWindow([remove_node_input_box], remove_node, function="remove_node", graph_algo=self.graph_algo)
        remove_node_button = Button(WHITE, WIDTH * 0.75, (HEIGHT * (1 / 9.0)) * 3, WIDTH * 0.25, HEIGHT * (1 / 9.0), "Remove Node", window=remove_node_window)

        src_add_edge_input_box = InputBox(10, 10, 65, 30, "Src", text_size=16)
        dest_add_edge_input_box = InputBox(80, 10, 65, 30, "Dest", text_size=16)
        weight_input_box = InputBox(150, 10, 65, 30, "Weight", text_size=16)
        add_edge = Button(WHITE, 220, 10, 80, 30, "Add", text_size=16)
        add_edge_window = LittleWindow([src_add_edge_input_box, dest_add_edge_input_box, weight_input_box], add_edge, function="add_edge", graph_algo=self.graph_algo)
        add_edge_button = Button(WHITE, WIDTH * 0.75, (HEIGHT * (1 / 9.0)) * 4, WIDTH * 0.25, HEIGHT * (1 / 9.0), "Add Edge", window=add_edge_window)

        src_remove_edge_input_box = InputBox(10, 10, 100, 30, "Src", text_size=16)
        dest_remove_edge_input_box = InputBox(115, 10, 100, 30, "Dest", text_size=16)
        remove_edge = Button(WHITE, 220, 10, 80, 30, "Remove", text_size=16)
        remove_edge_window = LittleWindow([src_remove_edge_input_box, dest_remove_edge_input_box], remove_edge, function="remove_edge", graph_algo=self.graph_algo)
        remove_edge_button = Button(WHITE, WIDTH * 0.75, (HEIGHT * (1 / 9.0)) * 5, WIDTH * 0.25, HEIGHT * (1 / 9.0), "Remove Edge", window=remove_edge_window)

        src_shortest_path_input_box = InputBox(10, 10, 100, 30, "Src", text_size=16)
        dest_shortest_path_input_box = InputBox(115, 10, 100, 30, "Dest", text_size=16)
        find_shortest_path = Button(WHITE, 220, 10, 80, 30, "Find", text_size=16)
        shortest_path_window = LittleWindow([src_shortest_path_input_box, dest_shortest_path_input_box], find_shortest_path, function="find_shortest_path", graph_algo=self.graph_algo)
        shortest_path_button = Button(WHITE, WIDTH * 0.75, (HEIGHT * (1 / 9.0)) * 6, WIDTH * 0.25, HEIGHT * (1 / 9.0), "Shortest Path", window=shortest_path_window)

        tsp_input_box = InputBox(10, 10, 200, 30, "Ids: 1,2,3.. or type All", text_size=16)
        tsp = Button(WHITE, 220, 10, 80, 30, "Find", text_size=16)
        tsp_window = LittleWindow([tsp_input_box], tsp, function="TSP", graph_algo=self.graph_algo)
        tsp_button = Button(WHITE, WIDTH * 0.75, (HEIGHT * (1 / 9.0)) * 7, WIDTH * 0.25, HEIGHT * (1 / 9.0), "TSP", window=tsp_window)

        center_point = Button(WHITE, 10, 10, 300, 35, "Find", text_size=24)
        center_point_window = LittleWindow([], center_point, function="centerPoint", graph_algo=self.graph_algo)
        center_point_button = Button(WHITE, WIDTH * 0.75, (HEIGHT * (1 / 9.0)) * 8, WIDTH * 0.25, HEIGHT * (1 / 9.0), "Center Node", window=center_point_window)

        return [load_button, save_button, add_node_button, remove_node_button, add_edge_button, remove_edge_button,
                shortest_path_button, tsp_button, center_point_button]
