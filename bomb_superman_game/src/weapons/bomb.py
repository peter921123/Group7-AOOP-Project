import os
image_path = [os.path.join(os.path.dirname(__file__), f"..\..\img\weapons\\bomb_{i}.png") for i in range(4)]

import pygame

from config import *
from mysprite import mysprite

class Bomb(mysprite.MySprite):

    all_bombs = pygame.sprite.Group()
    images_list = []

    class Explosion(mysprite.MySprite):

        all_explosions = pygame.sprite.Group()

        def __init__(self, pos_x, pos_y):
            super().__init__()
            self.image = pygame.Surface((grid_size, grid_size)) # 建立一個 surface
            self.image.fill((255, 255, 255)) # 填滿白色
            self.rect = self.image.get_rect() # 取得圖片矩形
            self.rect.x = pos_x
            self.rect.y = pos_y
            self.timer = pygame.time.get_ticks() # 計時器
            Bomb.Explosion.all_explosions.add(self)

        def update(self):
            if(pygame.time.get_ticks() - self.timer) > 500:
               self.kill()

        def kill(self):
            super().kill()

    @staticmethod
    def load_images():
        Bomb.images_list = [pygame.image.load(i).convert_alpha() for i in image_path] # 載入圖片
        Bomb.images_list = [pygame.transform.scale(i, (50, 50)) for i in Bomb.images_list] # 調整圖片大小

    @staticmethod
    def is_getting_bombed(character):
        direction = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        bombs = [bomb for bomb in Bomb.all_bombs if (pygame.time.get_ticks() - bomb.timer) < 1000]
        for bomb in Bomb.all_bombs:
            for i in range(4):
                for j in range(bomb.strength):
                    pos_x = bomb.rect.x + direction[i][0] * grid_size * (j + 1)
                    pos_y = bomb.rect.y + direction[i][1] * grid_size * (j + 1)
                    explosion = Bomb.Explosion(pos_x, pos_y)
                    collided_sprites = pygame.sprite.spritecollide(explosion, mysprite.MySprite.all_sprites, False)
                    explosion.kill()
                    if (character in collided_sprites):
                        return True
        return False

    def __init__(self, pos_x, pos_y, strength = 1):
        super().__init__()
        self.strength = strength # 炸彈威力
        self.timer = pygame.time.get_ticks() # 計時器
        self.image = pygame.Surface((50, 50)) # 建立一個 surface
        self.rect = self.image.get_rect() # 取得圖片矩形
        self.current_image = 0 # 目前圖片索引
        self.image = Bomb.images_list[self.current_image] # 載入圖片
        self.rect.x, self.rect.y = pos_x, pos_y # 設定圖片矩形位置
        Bomb.all_bombs.add(self)

    def update(self):
        if (pygame.time.get_ticks() - self.timer) <= 2000: # 計時器小於 2 秒，一般炸彈圖片更換
            image_update_rate = 0.1
        elif (pygame.time.get_ticks() - self.timer) < 3000: # 計時器介於 2 秒到 3 秒之間，炸彈圖片更換加快
            image_update_rate = 0.2
        else: # 計時器大於 3 秒，炸彈爆炸
            self.explode()
            return

        self.current_image += image_update_rate # 更新圖片索引
        if self.current_image >= len(Bomb.images_list):
            self.current_image = 0
        self.image = Bomb.images_list[int(self.current_image)] # 更新圖片

    def explode(self):
        direction = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for i in range(4):
            for j in range(self.strength):
                pos_x = self.rect.x + direction[i][0] * grid_size * (j + 1)
                pos_y = self.rect.y + direction[i][1] * grid_size * (j + 1)
                explosion = Bomb.Explosion(pos_x, pos_y)
                collided_sprites = pygame.sprite.spritecollide(explosion, mysprite.MySprite.all_sprites, False) # 檢查 Explosion 是否與其他 Sprite 碰撞
                for collided_sprite in collided_sprites: # 將碰撞到的 Sprite 中去掉自己與所有 Explosion Object
                    if (collided_sprite in Bomb.Explosion.all_explosions):
                        collided_sprites.remove(collided_sprite)
                if (len(collided_sprites) > 0):
                    for collided_sprite in collided_sprites:
                        if (collided_sprite not in Bomb.all_bombs): # 如果碰撞到的 Sprite 不是炸彈，則刪除
                            collided_sprite.kill()
                            # p.s. 一開始想嘗試實行連鎖引爆，但會出現重複呼叫和遞迴過深的問題，所以暫時先不實作。
                    break

        self.kill() # 從所有 Group 中移除此 Sprite
