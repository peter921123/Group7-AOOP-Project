import os
image_path = os.path.join(os.path.dirname(__file__), f"..\..\img\obstacles\\box.png")

import pygame

from config import *
from mysprite import mysprite
from obstacles import obstacle

class Box(obstacle.Obstacle):

    all_boxes = pygame.sprite.Group()

    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, grid_size, grid_size, True)
        print('Box init')

        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))

        Box.all_boxes.add(self)

    def kill(self):
        print("Box kill")
        super().kill()