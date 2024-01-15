import sys
import pygame
from pygame.locals import *

from character import character
from attribute import attribute
from config import *

pygame.init() # 初始化pygame
window_surface = pygame.display.set_mode(window_size) # 設定視窗大小
pygame.display.set_caption(window_caption) # 設定視窗標題
window_background = pygame.image.load(background_path).convert_alpha() # 載入背景圖片
window_background = pygame.transform.scale(window_background, window_size) # 調整背景圖片大小
window_surface.blit(window_background, (0, 0)) # 貼上背景圖片

character = character.Character() # 建立角色物件
character.set_pos(100, 100) # 設定角色位置
window_surface.blit(character.image, character.rect) # 繪製角色

# 更新畫面，等所有操作完成後一次更新（若沒更新，則元素不會出現）
pygame.display.update()

# 事件迴圈監聽事件，進行事件處理
while True:
    # 迭代整個事件迴圈，若有符合事件則對應處理
    for event in pygame.event.get():
        # 當使用者結束視窗，程式也結束
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                print('SPACE')
            elif event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[K_UP] or keys[K_w]:
            print('UP')
            character.move_up()
        if keys[K_DOWN] or keys[K_s]:
            print('DOWN')
            character.move_down()
        if keys[K_LEFT] or keys[K_a]:
            print('LEFT')
            character.move_left()
        if keys[K_RIGHT] or keys[K_d]:
            print('RIGHT')
            character.move_right()

        character.check_position()

        window_surface.blit(window_background, (0, 0))
        window_surface.blit(character.image, character.rect)
        pygame.display.update() # 更新畫面