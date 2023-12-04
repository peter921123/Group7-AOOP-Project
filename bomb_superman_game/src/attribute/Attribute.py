class Attribute():
    def __init__(self, speed = 10, strength = 1, hp = 3):
        self.speed = speed
        self.strength = strength
        self.hp = hp

    def get_strength(self):
        return self.strength

    def get_speed(self):
        return self.speed
    
    def get_hp(self):
        return self.hp

    def set_strength(self, strength):
        self.strength = strength
    
    def set_speed(self, speed):
        self.speed = speed

    def set_hp(self, hp = 1):
        self.hp = hp

