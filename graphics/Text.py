import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
SKY_BLUE = (75, 118, 229)
LIGHT_YELLOW = (255, 253, 126)


class Text:

    def __init__(self, x, y, text='', size=16, color=BLACK, font='comicsans'):
        self.x = x
        self.y = y
        self.size = size
        self.font = font
        self.text = text
        self.color = color

    def draw(self, screen, top_left: bool = False):
        font = pygame.font.SysFont(self.font, self.size)
        text = font.render(self.text, True, self.color)
        if top_left:
            screen.blit(text, (self.x, self.y))
        else:
            screen.blit(text, (self.x - text.get_width() / 2, self.y - text.get_height() / 2))
