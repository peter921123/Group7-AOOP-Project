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

    def __init__(self, pos_x, pos_y):
        super().__init__()
        mysprite.MySprite.__init__(self) # Don't know why the group doesn't work without this line.
        self.image = pygame.Surface((40, 40)) # 建立一個 surface
        self.rect = self.image.get_rect() # 取得圖片矩形
        self.image = pygame.image.load(image_path).convert_alpha() # 載入圖片
        self.image = pygame.transform.scale(self.image, (48, 48))
        # self.rect = self.image.get_rect() # 取得圖片矩形
        self.rect.x, self.rect.y = pos_x, pos_y # 設定圖片矩形位置
        self.placed_bomb = pygame.sprite.Group() # 建立一個用來保持 character 所放置的炸彈的 Group
        Character.all_characters.add(self)

    def update(self):
        self.check_position() # 檢查角色位置
        #self.set_pos(self.rect.x, self.rect.y) # 設定角色位置
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

        collided_sprites = pygame.sprite.spritecollide(self, mysprite.MySprite.all_sprites, False)
        just_placed_bomb = [sprite for sprite in collided_sprites if sprite in bomb.Bomb.all_bombs]

        if len(just_placed_bomb) >= 1: # 若移動前就碰撞到炸彈，可移動至非炸彈位置。
            old_center = self.rect.center
            self.rect.center = (self.rect.center[0] + direction_dict[direction][0] * self.get_speed(), self.rect.center[1] + direction_dict[direction][1] * self.get_speed())
            collided_sprites = pygame.sprite.spritecollide(self, mysprite.MySprite.all_sprites, False)
            collided_sprites = [sprite for sprite in collided_sprites if (sprite not in item.Item.all_items and sprite not in Character.all_characters and sprite not in bomb.Bomb.all_bombs)]
            if len(collided_sprites) >= 1:
                print("Character detect collision, can't move.")
                self.rect.center = old_center
                return False
        else: # 若移動後才碰撞到某個 sprite，則不可移動。
            old_center = self.rect.center
            self.rect.center = (self.rect.center[0] + direction_dict[direction][0] * self.get_speed(), self.rect.center[1] + direction_dict[direction][1] * self.get_speed())
            collided_sprites = pygame.sprite.spritecollide(self, mysprite.MySprite.all_sprites, False)
            collided_sprites = [sprite for sprite in collided_sprites if (sprite not in item.Item.all_items and sprite not in Character.all_characters)]
            if len(collided_sprites) >= 1:
                print("Character detect collision, can't move.")
                self.rect.center = old_center
                return False
        return True

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
            pos_x = round(self.rect.x / grid_size) * grid_size
            pos_y = round(self.rect.y / grid_size) * grid_size
            self.placed_bomb.add(bomb.Bomb(pos_x, pos_y, self.get_strength()))

    def kill(self):
        print("Character kill")
        super().kill()
        self.placed_bomb.empty()
        self.is_dead = True


