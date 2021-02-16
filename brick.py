from globals import WIDTH
from colorama import Back


class Brick():
    '''Class for the brick'''

    def __init__(self, pos, strength=1):
        self.length = 5
        self.strength = strength
        self.img = [[(self.get_color() + ' ' + Back.RESET)
                     for _ in range(self.length)]]
        self.pos = pos
        self.destroyed = False

    def get_color(self):
        if self.strength == 1:
            return Back.GREEN
        elif self.strength == 2:
            return Back.CYAN
        elif self.strength == 3:
            return Back.MAGENTA
        elif self.strength == 4:
            return Back.RED

    def collides_with(self, obj):
        if type(obj).__name__ == 'Ball':
            if obj.pos[1] != self.pos[1]:
                return False
            if obj.vel[0] > 0:
                if self.pos[0] <= obj.pos[0] <= self.pos[0] + self.length - 1 + obj.vel[0]:
                    return True
                return False
            elif obj.vel[0] < 0:
                if self.pos[0] + obj.vel[0] <= obj.pos[0] <= self.pos[0] + self.length - 1:
                    return True
                return False
            else:
                if self.pos[0] <= obj.pos[0] <= self.pos[0] + self.length - 1:
                    return True
                return False
        return False

    def take_damage(self):
        # Called when ball collides with brick
        if self.strength < 4:
            self.strength -= 1
        if self.strength == 0:
            self.destroyed = True
            return
        self.img = [[(self.get_color() + ' ' + Back.RESET)
                     for _ in range(self.length)]]
