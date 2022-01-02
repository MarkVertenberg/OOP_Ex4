import math

import pygame.draw

from src.graphics.NodePainter import NodePainter
from src.graphics.Text import Text

BLACK = (0, 0, 0)


class EdgePainter:

    def __init__(self, src: NodePainter, dest: NodePainter, weight, color=BLACK):
        self.src = src
        self.dest = dest
        self.start_x, self.start_y, self.stop_x, self.stop_y = self.start_pos()
        self.color = color
        self.text = Text(None, None, weight)
        self.over = False

    def start_pos(self):
        if self.dest.new_x and self.dest.new_y:
            dx = self.dest.new_x - self.src.new_x
            dy = self.dest.new_y - self.src.new_y
            if dx == 0:
                dx = 0.00001
            a = math.atan(abs(dy / dx))
            s_h = math.sin(a) * self.src.radius
            s_w = math.cos(a) * self.src.radius
            d_h = math.sin(a) * self.dest.radius
            d_w = math.cos(a) * self.dest.radius
            if dx >= 0 and dy >= 0:
                return self.src.new_x + s_w, self.src.new_y + s_h, self.dest.new_x - d_w, self.dest.new_y - d_h
            if dx >= 0 and dy <= 0:
                return self.src.new_x + s_w, self.src.new_y - s_h, self.dest.new_x - d_w, self.dest.new_y + d_h
            if dx <= 0 and dy >= 0:
                return self.src.new_x - s_w, self.src.new_y + s_h, self.dest.new_x + d_w, self.dest.new_y - d_h
            else:
                return self.src.new_x - s_w, self.src.new_y - s_h, self.dest.new_x + d_w, self.dest.new_y + d_h
        return None, None, None, None

    def draw(self, screen, outline=2):
        self.start_x, self.start_y, self.stop_x, self.stop_y = self.start_pos()
        if self.start_x:
            pygame.draw.line(screen, self.color, (self.start_x, self.start_y), (self.stop_x, self.stop_y), outline)
            triangle = self.triangle_pos(self.dest.radius * 0.8)
            pygame.draw.polygon(screen, self.color, triangle)
            #self.text.x = str(triangle[2][0])
            #self.text.y = str(triangle[2][1])
            #self.text.draw(screen, True)

    def triangle_pos(self, height_tmp):
        dx = self.stop_x - self.start_x
        dy = self.stop_y - self.start_y
        if dx == 0:
            dx = 0.00001
        a = math.atan(abs(dy / dx))
        h = height_tmp * 0.5 * math.cos(a)
        w = height_tmp * 0.5 * math.sin(a)
        d_h = math.sin(a) * height_tmp
        d_w = math.cos(a) * height_tmp
        if dx >= 0 and dy >= 0:
            temp_x = self.stop_x - d_w
            temp_y = self.stop_y - d_h
            x_1 = temp_x - w
            y_1 = temp_y + h
            x_2 = temp_x + w
            y_2 = temp_y - h
            return [(x_1, y_1), (self.stop_x, self.stop_y), (x_2, y_2)]
        if dx >= 0 and dy <= 0:
            temp_x = self.stop_x - d_w
            temp_y = self.stop_y + d_h
            x_1 = temp_x + w
            y_1 = temp_y + h
            x_2 = temp_x - w
            y_2 = temp_y - h
            return [(x_1, y_1), (self.stop_x, self.stop_y), (x_2, y_2)]
        if dx <= 0 and dy >= 0:
            temp_x = self.stop_x + d_w
            temp_y = self.stop_y - d_h
            x_1 = temp_x - w
            y_1 = temp_y - h
            x_2 = temp_x + w
            y_2 = temp_y + h
            return [(x_1, y_1), (self.stop_x, self.stop_y), (x_2, y_2)]
        else:
            temp_x = self.stop_x + d_w
            temp_y = self.stop_y + d_h
            x_1 = temp_x + w
            y_1 = temp_y - h
            x_2 = temp_x - w
            y_2 = temp_y + h
            return [(x_1, y_1), (self.stop_x, self.stop_y), (x_2, y_2)]

