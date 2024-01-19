import os
image_path = os.path.join(os.path.dirname(__file__), "..\..\img\character\character_normal.png")
import pygame
from config import *
from mysprite import mysprite
from attribute import attribute
from weapons import bomb
from items import item

class Character(attribute.Attribute, mysprite.MySprite):

    all_characters = pygame.sprite.Group()

    def __init__(self):
        super().__init__()
        mysprite.MySprite.__init__(self) # Don't know why the group doesn't work without this line.
        self.image = pygame.Surface((40, 40)) # 建立一個 surface
        self.rect = self.image.get_rect() # 取得圖片矩形
        self.image = pygame.image.load(image_path).convert_alpha() # 載入圖片
        self.image = pygame.transform.scale(self.image, (48, 48))
        # self.rect = self.image.get_rect() # 取得圖片矩形
        self.rect.x, self.rect.y = self.get_pos() # 設定圖片矩形位置
        self.placed_bomb = pygame.sprite.Group() # 建立一個用來保持 character 所放置的炸彈的 Group
        Character.all_characters.add(self)

    def update(self):
        self.check_position() # 檢查角色位置
        self.set_pos(self.rect.x, self.rect.y) # 設定角色位置
        self.set_current_bomb_number(len(self.placed_bomb)) # 檢查並更新角色目前放置的炸彈數量

    def check_position(self):
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > window_size[0] - self.rect.width:
            self.rect.x = window_size[0] - self.rect.width
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > window_size[1] - self.rect.height:
            self.rect.y = window_size[1] - self.rect.height

    def move(self, direction):
        direction_dict = {
            "up": [0, -1],
            "down": [0, 1],
            "left": [-1, 0],
            "right": [1, 0]
        }

        if len(pygame.sprite.spritecollide(self, mysprite.MySprite.all_sprites, False)) > 1:
            self.rect.center = (self.rect.center[0] + direction_dict[direction][0] * self.get_speed(), self.rect.center[1] + direction_dict[direction][1] * self.get_speed())
            return
        # 如果在移動前已經與某個 sprite 碰撞，則可移動。

        old_center = self.rect.center
        self.rect.center = (self.rect.center[0] + direction_dict[direction][0] * self.get_speed(), self.rect.center[1] + direction_dict[direction][1] * self.get_speed())
        collided_sprites = pygame.sprite.spritecollide(self, mysprite.MySprite.all_sprites, False)
        collided_sprites = [sprite for sprite in collided_sprites if sprite not in item.Item.all_items]
        if len(collided_sprites) > 1:
            print("Character detect collision, can't move.")
            self.rect.center = old_center
        # 若移動後才碰撞到某個 sprite，則不移動。

    def move_up(self):
        self.move("up")

    def move_down(self):
        self.move("down")

    def move_left(self):
        self.move("left")

    def move_right(self):
        self.move("right")

    def place_bomb(self):
        if (self.get_current_bomb_number() < self.get_max_bomb_number()):
            self.set_current_bomb_number(self.get_current_bomb_number() + 1)
            pos_x = round(self.get_pos()[0] / grid_size) * grid_size
            pos_y = round(self.get_pos()[1] / grid_size) * grid_size
            self.placed_bomb.add(bomb.Bomb(pos_x, pos_y, self.get_strength()))

    def kill(self):
        print("Character kill")
        super().kill()
        self.placed_bomb.empty()


