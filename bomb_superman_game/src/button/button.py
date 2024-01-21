import pygame

class Button:
    def __init__(self, text, pos, font, width):
        self.text = text
        self.pos = pos
        self.rect = pygame.Rect(0, 0, width, font.get_height() + 10)
        self.rect.center = pos
        self.button_font = font
        self.color = (0, 0, 0)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, 2)
        text_surface = self.button_font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(center = self.pos)
        surface.blit(text_surface, text_rect)

    def set_color(self, color):
        self.color = color

class Text:
    def __init__(self, text, pos, font):
        self.text = text
        self.pos = pos
        self.font = font
        self.color = (0, 0, 0)

    def draw(self, surface):
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(center = self.pos)
        surface.blit(text_surface, text_rect)