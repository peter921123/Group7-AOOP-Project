class Attribute():

    def __init__(self, speed = 2, strength = 1, max_bomb_number = 1, current_bomb_number = 0):
        self.speed = speed
        self.strength = strength
        self.max_bomb_number = max_bomb_number
        self.current_bomb_number = current_bomb_number
        self.is_dead = False

    def get_max_bomb_number(self):
        return self.max_bomb_number

    def get_current_bomb_number(self):
        return self.current_bomb_number

    def get_strength(self):
        return self.strength

    def get_speed(self):
        return self.speed

    def get_is_dead(self):
        return self.is_dead

    def set_max_bomb_number(self, max_bomb_number):
        self.max_bomb_number = max_bomb_number

    def set_current_bomb_number(self, current_bomb_number):
        self.current_bomb_number = current_bomb_number

    def set_strength(self, strength):
        self.strength = strength

    def set_speed(self, speed):
        self.speed = speed

