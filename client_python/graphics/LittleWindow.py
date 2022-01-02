from typing import List

import pygame

from src.DiGraph import Node
from src.graphics.InputBox import InputBox
from src.graphics.Text import Text

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
SKY_BLUE = (75, 118, 229)
LIGHT_YELLOW = (255, 253, 126)
RED = (255, 0, 0)


class LittleWindow:

    def __init__(self, input_boxes: List[InputBox] = None, button=None, related=None, function=None, graph_algo=None):
        self.related = related
        self.input_boxes = input_boxes
        self.button = button
        self.massage = Text(160, 60, "Text")
        self.function = function
        self.graph_algo = graph_algo
        if related:
            if self.button:
                self.button.x += self.related.x
                self.button.y += self.related.y
            if self.input_boxes:
                for input_box in self.input_boxes:
                    input_box.x += self.related.x
                    input_box.y += self.related.y
            self.massage.x += self.related.x
            self.massage.y += self.related.y

    def handle_event(self, event):
        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.related.is_over(pos):
                self.related.is_clicked = False
        if self.button:
            self.button.handle_event(event)
            if self.button.is_clicked:
                self.massage.color = BLACK
                has_input = True
                self.massage.text = ""
                for data in self.input_boxes:
                    if data.text.text == '':
                        self.massage.text += data.massage.text + " "
                        has_input = False
                        self.massage.color = RED
                self.massage.text += "missing"
                if has_input:
                    self.massage.text = "processing"
                    if self.graph_algo.get_graph():
                        try:
                            if self.go_to_function():
                                self.massage.color = GREEN
                                self.massage.text = "Done"
                            else:
                                self.massage.color = RED
                                self.massage.text = "Failure"
                        except Exception as e:
                            print(e)
                            self.massage.color = RED
                            self.massage.text = "Failure"
                    else:
                        self.massage.text = "There is no graph"
                self.button.is_clicked = False
        if self.input_boxes:
            for input_box in self.input_boxes:
                input_box.handle_event(event)

    def draw(self, screen, outline):
        if outline:
            pygame.draw.rect(screen, BLACK, self.related.get_rect(), outline)
        if self.massage.text != '':
            self.massage.draw(screen)
        if self.button:
            self.button.draw(screen, 2)
        if self.input_boxes:
            for input_box in self.input_boxes:
                input_box.draw(screen, 2)

    def reset_data(self):
        if self.input_boxes:
            for input_box in self.input_boxes:
                input_box.text.text = ''
        self.massage.text = ''

    def go_to_function(self):
        if self.function == "load_from_json":
            return self.graph_algo.load_from_json(self.input_boxes[0].text.text)
        if self.function == "save_to_json":
            self.show_path_in_graph([])
            return self.graph_algo.save_to_json(self.input_boxes[0].text.text)
        if self.function == "add_node":
            key = int(self.input_boxes[0].text.text)
            x = float(self.input_boxes[1].text.text)
            y = float(self.input_boxes[2].text.text)
            return self.graph_algo.get_graph().add_node(key, (x, y))
        if self.function == "remove_node":
            key = int(self.input_boxes[0].text.text)
            return self.graph_algo.get_graph().remove_node(key)
        if self.function == "add_edge":
            src = int(self.input_boxes[0].text.text)
            dest = int(self.input_boxes[1].text.text)
            weight = float(self.input_boxes[2].text.text)
            return self.graph_algo.get_graph().add_edge(src, dest, weight)
        if self.function == "remove_edge":
            src = int(self.input_boxes[0].text.text)
            dest = int(self.input_boxes[1].text.text)
            return self.graph_algo.get_graph().remove_edge(src, dest)
        if self.function == "find_shortest_path":
            src = int(self.input_boxes[0].text.text)
            dest = int(self.input_boxes[1].text.text)
            path = self.graph_algo.shortest_path(src, dest)[1]
            if len(path) > 0:
                self.show_path_in_graph(path)
                return True
            return False
        if self.function == "TSP":
            data = self.input_boxes[0].text.text
            list_cities = []
            if data.upper() == "ALL":
                list_cities = list(self.graph_algo.get_graph().get_all_v().keys())
            else:
                for key in data.split(","):
                    list_cities.append(int(key))
            path = self.graph_algo.TSP(list_cities)[0]
            if len(path) > 0:
                self.show_path_in_graph(path)
                return True
            return False
        if self.function == "centerPoint":
            ans = self.graph_algo.centerPoint()[0]
            if ans is not None:
                self.show_path_in_graph([ans])
                return True
            return False
        return False

    def show_path_in_graph(self, path: List[int]):
        nodes = self.graph_algo.get_graph().get_all_v().values()
        for node in nodes:
            node.painter.color = LIGHT_YELLOW
            node.painter.dest = None
            if path.__contains__(node.value):
                index = path.index(node.value)
                node.painter.color = GREEN
                if len(path) > index + 1:
                    node.painter.dest = path.__getitem__(index + 1)
