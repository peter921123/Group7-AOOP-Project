import sys
import pygame
from pygame.locals import *

from character import character
from attribute import attribute
from weapons import bomb
from config import *

pygame.init() # 初始化pygame

clock = pygame.time.Clock() # 建立遊戲時鐘

window_surface = pygame.display.set_mode(window_size) # 設定視窗大小
pygame.display.set_caption(window_caption) # 設定視窗標題
window_background = pygame.image.load(background_path).convert_alpha() # 載入背景圖片
window_background = pygame.transform.scale(window_background, window_size) # 調整背景圖片大小
window_surface.blit(window_background, (0, 0)) # 貼上背景圖片

player = character.Character() # 建立角色物件
player.set_pos(0, 0) # 設定角色位置
window_surface.blit(player.image, player.rect) # 繪製角色

bomb.Bomb.load_images() # 載入炸彈圖片

pygame.display.update() # 更新畫面

pygame.event.set_blocked(pygame.MOUSEMOTION) # 鎖定滑鼠游標

while True: # 事件迴圈監聽事件，進行事件處理

    clock.tick(60) # 遊戲迴圈每秒執行60次

    # all_sprites = pygame.sprite.Group() # 建立一個用來檢查所有 Sprite 的 Group

    for event in pygame.event.get(): # 迭代整個事件迴圈，若有符合事件則對應處理

        # 當使用者結束視窗，程式也結束
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                print('SPACE')
                player.place_bomb()
            elif event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    keys = pygame.key.get_pressed()

    if keys[K_UP] or keys[K_w]:
        print('UP')
        player.move_up()
    if keys[K_DOWN] or keys[K_s]:
        print('DOWN')
        player.move_down()
    if keys[K_LEFT] or keys[K_a]:
        print('LEFT')
        player.move_left()
    if keys[K_RIGHT] or keys[K_d]:
        print('RIGHT')
        player.move_right()

    window_surface.blit(window_background, (0, 0)) # 貼上背景圖片
    bomb.Bomb.all_bombs.update() # 更新炸彈圖片
    bomb.Bomb.all_bombs.draw(window_surface) # 繪製炸彈
    character.Character.all_characters.update() # 更新角色圖片
    character.Character.all_characters.draw(window_surface) # 繪製角色
    pygame.display.update() # 更新畫面