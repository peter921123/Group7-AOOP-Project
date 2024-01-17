import pygame
class MySprite(pygame.sprite.Sprite):

    all_sprites = pygame.sprite.Group()

    def __init__(self):
        print('MySprite init')
        super().__init__()
        MySprite.all_sprites.add(self)