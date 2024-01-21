import os
import random

import pygame

from config import *
from mysprite import mysprite
from character import character

class Item():

    all_items = pygame.sprite.Group()

    class BombStrengthIncreaseItem(mysprite.MySprite):

            def __init__(self, pos_x, pos_y):
                super().__init__()
                #print('BombStrengthIncreaseItem init')
                image_path = os.path.join(os.path.dirname(__file__), f"..\..\img\items\\bomb_strength_increase_item.png")
                self.image = pygame.Surface((40, 40))
                self.rect = self.image.get_rect()
                self.image = pygame.image.load(image_path).convert_alpha()
                self.image = pygame.transform.scale(self.image, (48, 48))
                self.rect.x, self.rect.y = pos_x, pos_y

                Item.all_items.add(self)

            def kill(self):
                #print("BombRangeIncreaseItem kill")
                super().kill()

            def update(self):
                collided_sprites = pygame.sprite.spritecollide(self, mysprite.MySprite.all_sprites, False)
                for collided_sprite in collided_sprites:
                    if isinstance(collided_sprite, character.Character):
                        self.funtion(collided_sprite)
                        self.kill()
                        break

            def funtion(self, character):
                character.set_strength(character.get_strength() + 1)

    class SpeedIncreaseItem(mysprite.MySprite):

            def __init__(self, pos_x, pos_y):
                super().__init__()
                #print('SpeedIncreaseItem init')
                image_path = os.path.join(os.path.dirname(__file__), f"..\..\img\items\\bomb_strength_increase_item.png")
                self.image = pygame.Surface((40, 40))
                self.rect = self.image.get_rect()
                self.image = pygame.image.load(image_path).convert_alpha()
                self.image = pygame.transform.scale(self.image, (48, 48))
                self.rect.x, self.rect.y = pos_x, pos_y

                Item.all_items.add(self)

            def kill(self):
                #print("SpeedIncreaseItem kill")
                super().kill()

            def update(self):
                collided_sprites = pygame.sprite.spritecollide(self, mysprite.MySprite.all_sprites, False)
                for collided_sprite in collided_sprites:
                    if isinstance(collided_sprite, character.Character):
                        self.funtion(collided_sprite)
                        self.kill()
                        break

            def funtion(self, character):
                character.set_speed(character.get_speed() + 1)

    class MaxBombNumberIcreaseItem(mysprite.MySprite):

            def __init__(self, pos_x, pos_y):
                super().__init__()
                #print('MaxBombNumberIcreaseItem init')
                image_path = os.path.join(os.path.dirname(__file__), f"..\..\img\items\\bomb_strength_increase_item.png")
                self.image = pygame.Surface((40, 40))
                self.rect = self.image.get_rect()
                self.image = pygame.image.load(image_path).convert_alpha()
                self.image = pygame.transform.scale(self.image, (48, 48))
                self.rect.x, self.rect.y = pos_x, pos_y

                Item.all_items.add(self)

            def kill(self):
                #print("MaxBombNumberIcreaseItem kill")
                super().kill()

            def update(self):
                collided_sprites = pygame.sprite.spritecollide(self, mysprite.MySprite.all_sprites, False)
                for collided_sprite in collided_sprites:
                    if isinstance(collided_sprite, character.Character):
                        self.funtion(collided_sprite)
                        self.kill()
                        break

            def funtion(self, character):
                character.set_max_bomb_number(character.get_max_bomb_number() + 1)

    def __init__(self):
        pass

    @staticmethod
    def item_generate(pos_x, pos_y):

        rand_num = random.random()
        if rand_num <= 0.1:
            Item.all_items.add(Item.BombStrengthIncreaseItem(pos_x, pos_y))
        elif 0.1 < rand_num <= 0.2:
            Item.all_items.add(Item.SpeedIncreaseItem(pos_x, pos_y))
        elif 0.2 < rand_num <= 0.3:
            Item.all_items.add(Item.MaxBombNumberIcreaseItem(pos_x, pos_y))
        else:
            return