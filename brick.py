from globals import WIDTH, RAINBOW_BLINK_INTERVAL
from colorama import Back
import time
import random

class Brick():
    '''Class for the brick'''

    def __init__(self, pos, strength=1):
        self.length = 5
        self.rainbow = (strength == 5)
        self.strength = random.randint(1,4) if strength == 5 else strength
        self.img = [[(self.get_color() + ' ' + Back.RESET)
                     for _ in range(self.length)]]
        self.pos = pos
        self.destroyed = False
        self.last_blink_time = time.time()

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

        elif type(obj).__base__.__name__ == 'PowerUp':
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
        
        elif type(obj).__name__ == 'Laser':
            if obj.pos[1] != self.pos[1]:
                return False
            if self.pos[0] <= obj.pos[0] <= self.pos[0] + self.length - 1:
                return True
            return False

        return False

    def take_damage(self):
        # Called when ball collides with brick
        if self.rainbow:
            self.rainbow = False
        if self.strength < 4:
            self.strength -= 1
        if self.strength == 0:
            self.destroyed = True
            return
        self.img = [[(self.get_color() + ' ' + Back.RESET)
                     for _ in range(self.length)]]

    def fall(self):
        # Move one step downwards
        self.pos[1] += 1

    def blink(self):
        # Change color and strength if rainbow
        if time.time() - self.last_blink_time > RAINBOW_BLINK_INTERVAL:
            self.last_blink_time = time.time()
            self.strength = ((self.strength) % 4 + 1)
            self.img = [[(self.get_color() + ' ' + Back.RESET)
                        for _ in range(self.length)]]