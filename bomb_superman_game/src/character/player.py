import pygame

from character import character

class Player(character.Character):

    all_players = pygame.sprite.Group()

    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        print('Player init')
        Player.all_players.add(self)

    def update(self):
        super().update()
