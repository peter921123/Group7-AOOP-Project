class Attribute():
    def __init__(self, speed = 10, strength = 1):
        self.speed = speed
        self.strength = strength
        self.pos_x = 0
        self.pos_y = 0

    def get_strength(self):
        return self.strength

    def get_speed(self):
        return self.speed
    
    def get_pos(self):
        return (self.pos_x, self.pos_y)

    def set_strength(self, strength):
        self.strength = strength
    
    def set_speed(self, speed):
        self.speed = speed

    def set_pos(self, x, y):
        self.pos_x = x
        self.pos_y = y

