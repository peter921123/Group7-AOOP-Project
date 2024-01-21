import sys

import pygame
from pygame.locals import *

from mysprite import mysprite
from character import character
from character import enemy
from character import player
from attribute import attribute
from weapons import bomb
from config import *
from obstacles import box
from factories import mapfactory
from button import button

class GameMode():
    def __init__(self):
        pygame.init() # 初始化pygame
        self.clock = pygame.time.Clock() # 建立遊戲時鐘
        self.window_surface = pygame.display.set_mode(window_size) # 設定視窗大小
        pygame.display.set_caption(window_caption) # 設定視窗標題

    def start_menu(self):
        self.button_font = pygame.font.SysFont(None, 40)
        self.title_font = pygame.font.SysFont(None, 60)
        self.start_button = button.Button("Start", (window_length / 2, window_width * 3 / 7), self.button_font, 150)
        self.title = button.Text("Bomb Man", (window_length / 2, window_width / 5), self.title_font)
        self.window_surface.fill((255, 255, 255)) # 設定視窗顏色為白色
        self.start_button.draw(self.window_surface)
        self.title.draw(self.window_surface)
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.start_button.rect.collidepoint(mouse_pos):
                        return
            pygame.display.update()

    def game_mode(self):

        self.window_background = pygame.image.load(background_path).convert_alpha() # 載入背景圖片
        self.window_background = pygame.transform.scale(self.window_background, window_size) # 調整背景圖片大小

        self.player = player.Player(pos_x = 0, pos_y = 0) # 建立角色物件
        self.window_surface.blit(self.player.image, self.player.rect) # 繪製角色

        self.enemy = enemy.Enemy(pos_x = 1000, pos_y = 800) # 建立敵人物件
        self.window_surface.blit(self.enemy.image, self.enemy.rect) # 繪製敵人

        bomb.Bomb.load_images() # 載入炸彈圖片

        self.map_factory = mapfactory.MapFactory() # 建立地圖工廠
        self.map_factory.create_map(1) # 建立地圖

        pygame.display.update() # 更新畫面

        pygame.event.set_blocked(pygame.MOUSEMOTION) # 鎖定滑鼠游標

        while True: # 事件迴圈監聽事件，進行事件處理

            self.clock.tick(60) # 遊戲迴圈每秒執行45次

            all_sprites = mysprite.MySprite.all_sprites # 建立一個用來保持所有 Sprite 的 Group

            for event in pygame.event.get(): # 迭代整個事件迴圈，若有符合事件則對應處理

                if event.type == QUIT: # 如果點擊關閉視窗則結束迴圈
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        print('SPACE')
                        self.player.place_bomb()
                    elif event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            keys = pygame.key.get_pressed()

            if keys[K_UP] or keys[K_w]:
                #print('UP')
                self.player.move_up()
            if keys[K_DOWN] or keys[K_s]:
                #print('DOWN')
                self.player.move_down()
            if keys[K_LEFT] or keys[K_a]:
                #print('LEFT')
                self.player.move_left()
            if keys[K_RIGHT] or keys[K_d]:
                #print('RIGHT')
                self.player.move_right()

            self.window_surface.blit(self.window_background, (0, 0)) # 貼上背景圖片
            all_sprites.update() # 更新所有 Sprite
            all_sprites.draw(self.window_surface) # 繪製所有 Sprite
            # bomb.Bomb.all_bombs.update() # 更新炸彈圖片
            # bomb.Bomb.all_bombs.draw(window_surface) # 繪製炸彈
            # character.Character.all_characters.update() # 更新角色圖片
            character.Character.all_characters.draw(self.window_surface) # 繪製角色
            pygame.display.update() # 更新畫面

            if (self.player.get_is_dead() or self.enemy.get_is_dead()):
                break

    def end_menu(self):

        #self.restart_button = button.Button("Restart", (window_length / 2, window_width * 3 / 7), self.button_font, 150)
        self.quit_button = button.Button("Quit", (window_length / 2, window_width * 4 / 7), self.button_font, 150)
        if self.player.get_is_dead():
            self.title = button.Text("You Lose", (window_length / 2, window_width / 5), self.title_font)
            self.window_surface.fill((255, 255, 255))
        elif self.enemy.get_is_dead():
            self.title = button.Text("You Win", (window_length / 2, window_width / 5), self.title_font)
            self.window_surface.fill((255, 255, 255))
        #self.restart_button.draw(self.window_surface)
        self.quit_button.draw(self.window_surface)
        self.title.draw(self.window_surface)
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.quit_button.rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
            pygame.display.update()

if __name__ == '__main__':
    game = GameMode()
    game.start_menu()
    game.game_mode()
    game.end_menu()

