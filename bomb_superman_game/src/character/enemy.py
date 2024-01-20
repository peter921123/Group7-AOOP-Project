import random

import pygame

from config import *
from character import character
from character import player
from weapons import bomb
from algorithms import algorithm
from items import item

class BehaviorNode:
    def __init__(self):
        pass

    def execute(self, enemy):
        if enemy.maximum_movement_per_frame == enemy.movement_counter:
            print("Enemy has reached maximum movement per frame")
            return

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

class IsCloseToPlayerNode(ConditionNode):
    def __init__(self):
        pass

    def execute(self, enemy):
        is_close_to_player = False
        for _ in player.Player.all_players:
            if not enemy.is_reachable(_):
                continue
            if enemy.get_distance_to_target(_) <= enemy.get_strength():
                is_close_to_player = True
                break
        print(f"檢查：是否靠近玩家 {is_close_to_player}")
        return is_close_to_player

class CanReachPlayerNode(ConditionNode):
    def __init__(self):
        pass

    def execute(self, enemy):
        can_reach_player = False
        for _ in player.Player.all_players:
            if enemy.is_reachable(_):
                can_reach_player = True
                break
        print(f"檢查：是否可以到達玩家 {can_reach_player}")
        return can_reach_player

class CanReachItemNode(ConditionNode):
    def __init__(self):
        pass

    def execute(self, enemy):
        can_reach_item = False
        for _ in item.Item.all_items:
            if enemy.is_reachable(_):
                can_reach_item = True
                break
        print(f"檢查：是否可以到達道具 {can_reach_item}")
        return can_reach_item
### End of Condition Nodes ###

### Action Nodes ###
class ActionNode(BehaviorNode):
    def __init__(self):
        pass

    def execute(self, enemy):
        super().execute(enemy)
        return True # 表示執行成功

class EscapeFromBombNode(ActionNode): # 之後要詳細實作逃離爆炸的方法
    def __init__(self):
        pass

    def execute(self, enemy):
        print("Enemy is escaping from bomb")
        enemy.move_randomly()
        super().execute(enemy)

class PlaceBombNode(ActionNode):
    def __init__(self):
        pass

    def execute(self, enemy):
        print("Enemy is placing bomb")
        enemy.place_bomb()
        super().execute(enemy)

class PickUpItemNode(ActionNode):
    def __init__(self):
        pass

    def execute(self, enemy):
        print("Enemy is picking up item")
        for _ in item.Item.all_items:
            if enemy.is_reachable(_):
                enemy.move_towards_target(_)
                break
        super().execute(enemy)

class ChasePlayerNode(ActionNode): #尚未實作 Player Class, 待補
    def __init__(self):
        pass

    def execute(self, enemy):
        print("Enemy is chasing player")
        for _ in player.Player.all_players:
            if enemy.is_reachable(_):
                enemy.move_towards_target(_)
                break
        super().execute(enemy)

### End of Action Nodes ###

class Enemy(character.Character):

    all_enemies = pygame.sprite.Group()

    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        Enemy.all_enemies.add(self)
        self.maximum_movement_per_frame = 30
        self.movement_counter = 0
        self.update_counter = 0
        self.behavior_tree = SelectorNode([
            SequenceNode([
                IsGettingBombedNode(),
                EscapeFromBombNode()
            ]),
            SequenceNode([
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
            ]) #,
            #DestroyBlockOnShortestPathNode()
        ])


    def update(self):
        self.update_counter += 1
        if self.update_counter % 30 == 0:
            self.movement_counter = 0
            self.behavior_tree.execute(self)
        super().update()

    def is_reachable(self, target): # 檢查 spriteA 是否可以到達 spriteB
        return algorithm.a_star(self, target) is not None

    def move_randomly(self):
        direction = random.choice(["up", "down", "left", "right"])
        self.move(direction)
        self.increase_movement_counter()

    def move_to_grid(self, grid_x, grid_y):
        while self.rect.x != grid_x or self.rect.y != grid_y and self.movement_counter < self.maximum_movement_per_frame:
            if grid_x > self.rect.x:
                self.move_right()
            elif grid_x < self.rect.x:
                self.move_left()
            elif grid_y > self.rect.y:
                self.move_down()
            elif grid_y < self.rect.y:
                self.move_up()
            self.increase_movement_counter()

    def move_towards_target(self, target):
        path = algorithm.a_star(self, target)
        if path is None:
            return
        print(path)
        for next_x, next_y in path:
            self.move_to_grid(next_x, next_y)
            if self.movement_counter >= self.maximum_movement_per_frame:
                break

    def get_distance_to_target(self, target):
        return algorithm.get_distance(self, target)

    def increase_movement_counter(self):
        self.movement_counter += 1

