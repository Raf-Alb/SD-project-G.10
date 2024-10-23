# player.py

class Player:
    def __init__(self, floor, gravity):
        self.y = floor
        self.y_speed = 0
        self.jumping = 0
        self.floor = floor
        self.gravity = gravity

    def jump(self):
        if self.jumping == 0:
            self.y_speed = -20
            self.jumping = 1
        elif self.jumping == 1 and self.y_speed >= 0:
            self.y_speed = -15
            self.jumping = 2
        elif self.jumping == 2 and self.y_speed >= 0:
            self.y_speed = -15
            self.jumping = 3

    def update(self):
        self.y_speed += self.gravity
        self.y = min(self.y + self.y_speed, self.floor)
        if self.y == self.floor:
            self.jumping = 0
            self.y_speed = 0