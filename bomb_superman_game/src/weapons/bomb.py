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

    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.Surface((50, 50)) # 建立一個 surface
        self.rect = self.image.get_rect() # 取得圖片矩形
        self.current_image = 0 # 目前圖片索引
        self.image = Bomb.images_list[self.current_image] # 載入圖片
        self.rect.x, self.rect.y = pos_x, pos_y # 設定圖片矩形位置
        Bomb.all_bombs.add(self)

    def update(self):
        self.current_image += 0.2
        if self.current_image >= len(Bomb.images_list):
            self.current_image = 0
        self.image = Bomb.images_list[int(self.current_image)] # 載入圖片
