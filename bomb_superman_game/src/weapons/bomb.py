import os
image_path = [os.path.join(os.path.dirname(__file__), f"..\..\img\weapons\\bomb_{i}.png") for i in range(4)]
import pygame

class Bomb(pygame.sprite.Sprite):

    all_bombs = pygame.sprite.Group()
    images_list = []

    @staticmethod
    def load_images():
        Bomb.images_list = [pygame.image.load(i).convert_alpha() for i in image_path] # 載入圖片
        Bomb.images_list = [pygame.transform.scale(i, (50, 50)) for i in Bomb.images_list] # 調整圖片大小

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
        self.kill() # 從所有 Group 中移除此 Sprite
