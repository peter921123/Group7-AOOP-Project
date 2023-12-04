class Attribute():
    def __init__(self, speed = 10, strength = 1):
        self.speed = speed
        self.strength = strength

    def get_strength(self):
        return self.strength
    def get_speed(self):
        return self.speed
    def set_strength(self, strength):
        self.strength = strength
    def set_speed(self, speed):
        self.speed = speed


