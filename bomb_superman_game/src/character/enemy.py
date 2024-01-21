import random

import pygame

from config import *
from character import character
from character import player
from weapons import bomb
from algorithms import algorithm
from items import item
from obstacles import box

class BehaviorNode:
    def __init__(self):
        pass

    def execute(self, enemy):
        if enemy.maximum_movement_per_frame == enemy.movement_counter:
            print("Enemy has reached maximum movement per frame")
            return True

class SequenceNode(BehaviorNode):
    def __init__(self, nodes):
        self.nodes = nodes

    def execute(self, enemy):
        for node in self.nodes:
            if not node.execute(enemy):
                return False
        super().execute(enemy)
        return True

class SelectorNode(BehaviorNode):
    def __init__(self, nodes):
        self.nodes = nodes

    def execute(self, enemy):
        for node in self.nodes:
            if node.execute(enemy):
                super().execute(enemy)
                return True
        return False

### Condition Nodes ###
class ConditionNode(BehaviorNode):
    def __init__(self):
        pass

    def execute(self, enemy):
        pass

class IsGettingBombedNode(ConditionNode):
    def __init__(self):
        pass

    def execute(self, enemy):
        is_getting_bombed = bomb.Bomb.is_getting_bombed(enemy)
        print(f"檢查：是否有炸彈會炸到自己 {is_getting_bombed}")
        return is_getting_bombed

class IsJustPlacedBombNode(ConditionNode):
    def __init__(self):
        pass

    def execute(self, enemy):
        is_just_placed_bomb = enemy.is_just_placed_bomb
        print(f"檢查：是否剛放置炸彈 {is_just_placed_bomb}")
        return is_just_placed_bomb

class IsCloseToPlayerNode(ConditionNode):
    def __init__(self):
        pass

    def execute(self, enemy):
        is_close_to_player = False
        if enemy.can_reach_player and enemy.get_distance_to_target(enemy.target_player) <= enemy.get_strength():
            is_close_to_player = True
        print(f"檢查：是否靠近玩家 {is_close_to_player}")
        return is_close_to_player

class CanReachPlayerNode(ConditionNode):
    def __init__(self):
        pass

    def execute(self, enemy):
        can_reach_player = False
        target_player = None
        for _ in player.Player.all_players:
            if enemy.is_reachable(_):
                target_player = _
                can_reach_player = True
                break
        print(f"檢查：是否可以到達玩家 {can_reach_player}")
        enemy.can_reach_player = can_reach_player
        enemy.target_player = target_player
        return can_reach_player

class CanReachItemNode(ConditionNode):
    def __init__(self):
        pass

    def execute(self, enemy):
        can_reach_item = False
        target_item = None
        for _ in item.Item.all_items:
            if enemy.is_reachable(_):
                can_reach_item = True
                target_item = _
                break
        enemy.can_reach_item = can_reach_item
        enemy.target_item = target_item
        print(f"檢查：是否可以到達道具 {can_reach_item}")
        return can_reach_item

class IsCloseToBoxNode(ConditionNode):
    def __init__(self):
        pass

    def execute(self, enemy):
        is_close_to_box = False
        direction = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dir in direction:
            for i in range(1, enemy.get_strength() + 1):
                next_x, next_y = round(enemy.rect.x / grid_size) * grid_size + dir[0] * grid_size * i, round(enemy.rect.y / grid_size) * grid_size + dir[1] * grid_size * i
                if not algorithm.is_inside_window(next_x, next_y):
                    break

                if algorithm.is_obstacle(next_x, next_y):
                    is_close_to_box = True

        print(f"檢查：是否靠近箱子 {is_close_to_box}")
        return is_close_to_box

### End of Condition Nodes ###

### Action Nodes ###
class ActionNode(BehaviorNode):
    def __init__(self):
        pass

    def execute(self, enemy):
        super().execute(enemy)
        return True # 表示執行成功

class EscapeFromExplosionNode(ActionNode):
    def __init__(self):
        pass

    def execute(self, enemy):
        nearest_grid_not_exploded = algorithm.nearest_grid_not_exploded(enemy)
        if nearest_grid_not_exploded is None:
            return False
        print("Enemy is escaping from exlplosion")
        enemy.move_to_grid(nearest_grid_not_exploded[0], nearest_grid_not_exploded[1])
        return True

class EscapeFromBombNode(ActionNode):
    def __init__(self):
        pass
    def execute(self, enemy):
        nearest_grid = enemy.find_nearest_grid()
        if nearest_grid is None:
            return False
        print("Enemy is escaping from bomb")
        enemy.move_to_grid(nearest_grid[0], nearest_grid[1])
        if (not pygame.sprite.spritecollide(enemy, bomb.Bomb.all_bombs, False)):
            enemy.is_just_placed_bomb = False
        return True


class PlaceBombNode(ActionNode):
    def __init__(self):
        pass

    def execute(self, enemy):
        if (enemy.get_current_bomb_number() >= enemy.get_max_bomb_number()):
            print("Enemy can't place bomb")
            return True
        print("Enemy is placing bomb")
        enemy.place_bomb()
        enemy.is_just_placed_bomb = True
        enemy.target_box = None
        return True

class PickUpItemNode(ActionNode):
    def __init__(self):
        pass

    def execute(self, enemy):
        print("Enemy is picking up item")
        enemy.move_towards_target(enemy.target_item)
        return True

class ChasePlayerNode(ActionNode):
    def __init__(self):
        pass

    def execute(self, enemy):
        print("Enemy is chasing player")
        for _ in player.Player.all_players:
            if enemy.is_reachable(_):
                enemy.move_towards_target(_)
                break
        return True

class GetCloseToNearestBoxNode(ActionNode):
    def __init__(self):
        pass

    def execute(self, enemy):
        enemy.find_nearest_box()
        if (enemy.target_box is None):
            print("Enemy can't find nearest box")
            return False
        if (algorithm.is_getting_bombed(enemy.target_box.rect.x, enemy.target_box.rect.y)):
            print("Enemy can't reach box because it will get bombed")
            return False
        print("Enemy is getting close to nearest box")
        enemy.move_to_grid(enemy.target_box.rect.x, enemy.target_box.rect.y)
        return True

### End of Action Nodes ###

class Enemy(character.Character):

    all_enemies = pygame.sprite.Group()

    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        Enemy.all_enemies.add(self)
        self.maximum_movement_per_frame = 1
        self.movement_counter = 0
        self.update_counter = 0
        self.can_reach_player = False
        self.target_player = None
        self.can_reach_item = False
        self.target_item = None
        self.target_box = None
        self.is_just_placed_bomb = False
        self.behavior_tree = SelectorNode([
            SequenceNode([
                IsGettingBombedNode(),
                EscapeFromExplosionNode()
            ]),
            SequenceNode([
                IsJustPlacedBombNode(),
                EscapeFromBombNode()
            ]),
            SequenceNode([
                CanReachPlayerNode(),
                IsCloseToPlayerNode(),
                PlaceBombNode()
            ]),
            SequenceNode([
                CanReachPlayerNode(),
                ChasePlayerNode()
            ]),
            SequenceNode([
                CanReachItemNode(),
                PickUpItemNode()
            ]),
            SequenceNode([
                IsCloseToBoxNode(),
                PlaceBombNode()
            ]),
            GetCloseToNearestBoxNode()
        ])


    def update(self):
        self.update_counter += 1
        if self.update_counter % 15 == 0:
            self.movement_counter = 0
            self.behavior_tree.execute(self)
            print(f"Enemy is at ({self.rect.x}, {self.rect.y})")
        super().update()

    def is_reachable(self, target): # 檢查 spriteA 是否可以到達 spriteB
        return algorithm.a_star(self, target) is not None

    def move_randomly(self):
        direction = random.choice(["up", "down", "left", "right"])
        self.move(direction)
        self.increase_movement_counter()

    def move_to_grid(self, grid_x, grid_y):
        #fail_attempt = [False, False, False, False]
        fail_attempt = 0
        while self.rect.x != grid_x or self.rect.y != grid_y and self.movement_counter < self.maximum_movement_per_frame:
            if fail_attempt >= 16 * self.maximum_movement_per_frame:
                return False
            '''
            if grid_x > self.rect.x and not fail_attempt[0]:
                if not self.move_right():
                    fail_attempt[0] = True
                self.increase_movement_counter()
            elif grid_x < self.rect.x and not fail_attempt[1]:
                if not self.move_left():
                    fail_attempt[1] = True
                self.increase_movement_counter()
            if grid_y > self.rect.y and not fail_attempt[2]:
                if not self.move_down():
                    fail_attempt[2] = True
                self.increase_movement_counter()
            elif grid_y < self.rect.y and not fail_attempt[3]:
                if not self.move_up():
                    fail_attempt[3] = True
                self.increase_movement_counter()
            '''

            if grid_x > self.rect.x:
                if not self.move_right():
                    fail_attempt += 1
                else:
                    self.increase_movement_counter()
            elif grid_x < self.rect.x:
                if not self.move_left():
                    fail_attempt += 1
                else:
                    self.increase_movement_counter()
            if grid_y > self.rect.y:
                if not self.move_down():
                    fail_attempt += 1
                else:
                    self.increase_movement_counter()
            elif grid_y < self.rect.y:
                if not self.move_up():
                    fail_attempt += 1
                else:
                    self.increase_movement_counter()

    def move_towards_target(self, target):
        path = algorithm.a_star(self, target)
        if path is None:
            return False

        for next_x, next_y in path:

            '''
            if algorithm.is_getting_bombed(next_x, next_y):
                print (next_x, next_y, "is getting bombed")
                return False
            '''
            print(f"Enemy is moving towards target ({next_x}, {next_y})")
            self.move_to_grid(next_x, next_y)
            if self.movement_counter >= self.maximum_movement_per_frame:
                return True
        return True

    def get_distance_to_target(self, target):
        return algorithm.get_distance(self, target)

    def increase_movement_counter(self):
        self.movement_counter += 1

    def find_nearest_box(self):
        min_distance = float('inf')
        nearest_box = None
        for _ in box.Box.all_boxes:
            distance = ((self.rect.x - _.rect.x)**2 + (self.rect.y - _.rect.y)**2)**0.5
            if distance < min_distance:
                min_distance = distance
                nearest_box = _
        self.target_box = nearest_box

    def find_nearest_grid(self):
        min_distance = float('inf')
        nearest_grid = None
        for i in range(1, 4):
            for dx, dy in [(-grid_size, 0), (grid_size, 0), (0, -grid_size), (0, grid_size)]:
                next_x, next_y = self.rect.x + dx * i, self.rect.y + dy * i
                if not algorithm.is_inside_window(next_x, next_y) or algorithm.is_blocked(next_x, next_y):
                    continue

                distance = ((self.rect.x - next_x)**2 + (self.rect.y - next_y)**2)**0.5
                if distance < min_distance:
                    min_distance = distance
                    nearest_grid = (next_x, next_y)
        return nearest_grid

