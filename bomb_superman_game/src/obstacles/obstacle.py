import pygame

from config import *
from mysprite import mysprite

class Obstacle(mysprite.MySprite):

    all_obstacles = pygame.sprite.Group()

    def __init__(self, pos_x, pos_y, width, height, destroyable = False):
        super().__init__()
        print('Obstacle init')

        self.image = pygame.Surface((width, height)) # 建立一個 surface
        self.rect = self.image.get_rect() # 取得圖片矩形
        self.rect.x = pos_x
        self.rect.y = pos_y

        self.destroyable = destroyable
        Obstacle.all_obstacles.add(self)

    def update(self):
        pass

    def kill(self):
        print("Obstacle kill")
        super().kill()

    def is_destroyable(self):
        return self.destroyable

    def set_destroyable(self, destroyable):
        self.destroyable = destroyable