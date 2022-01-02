import pygame

from src.graphics.Text import Text

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (75, 118, 229)


class InputBox:
    """
        Class that representing input box in pygame.
    """

    def __init__(self, x, y, width, height, massage='', text='', color=WHITE, color_outline=BLACK, text_size=16, text_color=BLACK):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.massage = Text(x, y, massage, text_size, text_color)
        self.text = Text(x, y, text, text_size, text_color)
        self.color = color
        self.color_outline = color_outline
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.is_over(pos):
                self.active = True
                self.color_outline = SKY_BLUE
            else:
                self.active = False
                self.color_outline = BLACK
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text.text = self.text.text[:-1]
                else:
                    self.text.text += event.unicode

    def draw(self, screen, outline=None):
        if outline:
            pygame.draw.rect(screen, self.color_outline, (self.x, self.y, self.width, self.height), outline)
            pygame.draw.rect(screen, self.color, (self.x + outline, self.y + outline, self.width - (outline * 2), self.height - (outline * 2)))
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

        self.reset_pos_text()
        if self.text.text != '':
            self.text.draw(screen, top_left=True)
        elif not self.active and self.massage.text != '':
            self.massage.draw(screen, top_left=True)

    def is_over(self, pos):
        """ Pos is the mouse position or a tuple of (x,y) coordinates,
            returns if the pos is over this input box """
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False

    def reset_pos_text(self):
        self.text.x = self.x + 5
        self.text.y = self.y + 5
        self.massage.x = self.x + 5
        self.massage.y = self.y + 5
