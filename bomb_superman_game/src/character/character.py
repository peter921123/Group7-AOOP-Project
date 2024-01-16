import os
image_path = os.path.join(os.path.dirname(__file__), "..\..\img\character\character_normal.png")
import pygame
from config import *
from attribute import attribute
from weapons import bomb

class Character(attribute.Attribute, pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50)) # 建立一個 surface
        self.image = pygame.image.load(image_path).convert_alpha() # 載入圖片
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect() # 取得圖片矩形
        self.rect.x, self.rect.y = self.get_pos() # 設定圖片矩形位置

    def check_position(self):
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > window_size[0] - self.rect.width:
            self.rect.x = window_size[0] - self.rect.width
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > window_size[1] - self.rect.height:
            self.rect.y = window_size[1] - self.rect.height

    def move_up(self):
        self.rect.y -= self.get_speed()
        self.set_pos(self.rect.x, self.rect.y)

    def move_down(self):
        self.rect.y += self.get_speed()
        self.set_pos(self.rect.x, self.rect.y)

    def move_left(self):
        self.rect.x -= self.get_speed()
        self.set_pos(self.rect.x, self.rect.y)

    def move_right(self):
        self.rect.x += self.get_speed()
        self.set_pos(self.rect.x, self.rect.y)

    def place_bomb(self):
        if (self.get_current_bomb_number() < self.get_max_bomb_number()):
            self.set_current_bomb_number(self.get_current_bomb_number() + 1)
            bomb.Bomb(self.get_pos()[0], self.get_pos()[1])




