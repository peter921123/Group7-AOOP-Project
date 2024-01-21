import heapq

import pygame

from mysprite import mysprite
from obstacles import obstacle
from character import character
from items import item
from weapons import bomb

grid_size = 50
window_width = 1000
window_height = 800

def is_inside_window(x, y):
    return 0 <= x < window_width and 0 <= y < window_height

def is_obstacle(x, y):
    grid = pygame.Rect(x, y, grid_size, grid_size)
    for o in obstacle.Obstacle.all_obstacles:
        if grid.colliderect(o.rect):
            return True
    return False

def is_blocked(x, y):
    grid = pygame.Rect(x, y, grid_size, grid_size)
    collided_sprites = [sprite for sprite in mysprite.MySprite.all_sprites if grid.colliderect(sprite.rect)]
    collided_sprites = [sprite for sprite in collided_sprites if (sprite not in item.Item.all_items and sprite not in character.Character.all_characters)]
    if len(collided_sprites) >= 1:
        return True
    return False

def is_getting_bombed(x, y):
    temp = mysprite.MySprite()
    temp.rect = pygame.Rect(x, y, grid_size, grid_size)
    if bomb.Bomb.is_getting_bombed(temp):
        temp.kill()
        print (f"This grid {x, y} is getting bombed.")
        return True
    temp.kill()
    return False

class Node:
    def __init__(self, x, y, cost, prev):
        self.x = x
        self.y = y
        self.cost = cost
        self.prev = prev

    def __lt__(self, other):
        return self.cost < other.cost

def heuristic(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)

def nearest_grid_not_exploded(start):
    for i in range(1, 4):
        for dx, dy in [(-grid_size, 0), (grid_size, 0), (0, -grid_size), (0, grid_size)]:
            next_x, next_y = start.rect.x + dx * i, start.rect.y + dy * i
            if not is_inside_window(next_x, next_y) or is_blocked(next_x, next_y):
                continue

            if is_getting_bombed(next_x, next_y):
                continue
            '''
            temp = pygame.sprite.Sprite()
            temp.rect = pygame.Rect(next_x, next_y, grid_size, grid_size)
            if bomb.Bomb.is_getting_bombed(temp):
                continue
            temp.kill()
            '''
            print (f"Nearest grid not exploded is {next_x, next_y}")
            return (next_x, next_y)
    return None

def a_star(start, goal):
    open_list = []
    closed_list = set()

    start_node = Node(round(start.rect.x / grid_size) * grid_size, round(start.rect.y / grid_size) * grid_size, 0, None)
    goal_node = Node(round(goal.rect.x / grid_size) * grid_size, round(goal.rect.y / grid_size) * grid_size, 0, None)

    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)
        closed_list.add((current_node.x, current_node.y))
        if current_node.x == goal_node.x and current_node.y == goal_node.y:
            path = []
            while current_node is not None:
                path.append((current_node.x, current_node.y))
                current_node = current_node.prev
            return path[::-1]

        for dx, dy in [(-grid_size, 0), (grid_size, 0), (0, -grid_size), (0, grid_size)]:
            next_x, next_y = current_node.x + dx, current_node.y + dy
            if not is_inside_window(next_x, next_y) or is_blocked(next_x, next_y) or (next_x, next_y) in closed_list:
                continue
            next_node = Node(next_x, next_y, current_node.cost + 1 + heuristic(goal_node, current_node), current_node)
            heapq.heappush(open_list, next_node)

    return None

def get_distance(a, b):
    if a_star(a, b) is None:
        return None
    return len(a_star(a, b))