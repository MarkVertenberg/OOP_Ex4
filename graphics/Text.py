import pygame

from Colors import *
from api.ScreenObjectInterface import ScreenObjectInterface


class Text(ScreenObjectInterface):

    def __init__(self, x, y, text='', size=16, color=BLACK, font='comicsans'):
        self.x = x
        self.y = y
        self.size = size
        self.font = font
        self.text = text
        self.color = color

    def draw(self, screen, outline=None):
        font = pygame.font.SysFont(self.font, self.size)
        text = font.render(self.text, True, self.color)
        screen.blit(text, (self.x - text.get_width() / 2, self.y - text.get_height() / 2))
