import pygame
from attribute import attribute

class Character(attribute.Attribute, pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

