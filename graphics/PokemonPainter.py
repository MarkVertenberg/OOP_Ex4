import pygame

from OOP_Ex4.client_python.pokemon import Pokemon
from OOP_Ex4.graphics.Text import Text
from OOP_Ex4.graphics.Scale import Scale
from OOP_Ex4.graphics.api import *
from OOP_Ex4.graphics.Colors import *


class PokemonPainter(ScreenObjectInterface, Scalable):

    def __init__(self, pokemon: Pokemon, radius=12, color=LIGHT_RED):
        self.pokemon = pokemon
        self.radius = radius
        self.color = color
        self.text = Text(pokemon.x, pokemon.y, str(pokemon.value), 14)
        self.new_x = None
        self.new_y = None

    def draw(self, screen, outline=None):
        if self.new_x and self.new_y:
            self.text.x = self.new_x
            self.text.y = self.new_y
            if outline:
                pygame.draw.circle(screen, BLACK, (self.new_x, self.new_y), self.radius + outline)
            pygame.draw.circle(screen, self.color, (self.new_x, self.new_y), self.radius)
            self.text.draw(screen)

    def handle_event(self, event):
        pass

    def scale(self, scaler: Scale):
        pixel_x, pixel_y = scaler.calculate_pixel()
        if pixel_x == 0:
            pixel_x = 0.00001
        if pixel_y == 0:
            pixel_y = 0.00001
        self.new_x = ((self.pokemon.x - scaler.min_x) / pixel_x) + scaler.start_x
        self.new_y = ((self.pokemon.y - scaler.min_y) / pixel_y) + scaler.start_y

    def get_size(self):
        return self.radius
