#
# @file __init__.py
#

import pygame
import os

background_path = os.path.join(os.path.dirname(__file__), "..\..\img\\background\\background.png") # 背景圖片路徑

window_length = 800 # 視窗長度
window_width = 600 # 視窗寬度
window_size = (window_length, window_width) # 視窗大小
window_caption = "Bomb Superman" # 視窗標題