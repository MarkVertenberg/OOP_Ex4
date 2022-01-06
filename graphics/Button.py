import pygame
from graphics.Text import Text
from graphics.Colors import *
from graphics.api.ScreenObjectInterface import ScreenObjectInterface


class Button(ScreenObjectInterface):
    """
        Class that representing a button in pygame.
    """

    def __init__(self, color, x, y, width, height, text='', text_color=BLACK, text_size=48, function=None):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = Text(x + (width / 2), y + (height / 2), text, text_size, text_color)
        self.is_clicked = False
        self.function = function

    def handle_event(self, event):
        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_over(pos):
                print(self.text.text + " button is clicked!")
                self.is_clicked = True
                self.function()
        if event.type == pygame.MOUSEMOTION:
            if self.is_over(pos):
                self.text.color = LIGHT_RED
            else:
                self.text.color = BLACK

    def draw(self, screen, outline=None):
        if outline:
            pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), outline)
            pygame.draw.rect(screen, self.color, (self.x + outline, self.y + outline, self.width - (outline * 2), self.height - (outline * 2)))
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

        if self.text != '':
            self.text.x = self.x + (self.width / 2)
            self.text.y = self.y + (self.height / 2)
            self.text.draw(screen)

    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False

    def get_rect(self):
        return self.x, self.y, self.width, self.height
