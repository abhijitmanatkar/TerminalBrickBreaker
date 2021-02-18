from globals import WIDTH, BALL_MAX_X_SPEED, MAX_PADDLE_SIZE, MIN_PADDLE_SIZE
from colorama import Back


class Paddle():
    '''Class for the paddle'''

    def __init__(self, pos):
        self.length = 7
        self.img = [[(Back.BLUE + ' ' + Back.RESET)
                     for _ in range(self.length)]]
        self.pos = pos
        self.speed = 2
        self.grab = False

    def move(self, dir):
        old_x = self.pos[0]
        if dir == "d":
            if (self.pos[0] + self.length + 1 <= WIDTH):
                self.pos[0] += self.speed
        elif dir == "a":
            if (self.pos[0] > 1):
                self.pos[0] -= self.speed

        return self.pos[0] - old_x

    def collides_with(self, obj):
        if type(obj).__name__ == 'Ball':
            if obj.pos[1] != self.pos[1]:
                return False
            if obj.vel[0] >= 0:
                if self.pos[0] <= obj.pos[0] <= self.pos[0] + self.length - 1 + obj.vel[0]:
                    return True
                return False
            else:
                if self.pos[0] + obj.vel[0] <= obj.pos[0] <= self.pos[0] + self.length - 1:
                    return True
                return False
        elif type(obj).__base__.__name__ == 'PowerUp':
            if obj.pos[1] != self.pos[1]:
                return False
            if self.pos[0] <= obj.pos[0] <= self.pos[0] + self.length - 1:
                return True
            return False
        return False

    def expand(self):
        self.length = min(self.length + 2, MAX_PADDLE_SIZE)
        self.img = [[(Back.BLUE + ' ' + Back.RESET)
                     for _ in range(self.length)]]

    def shrink(self):
        self.length = max(self.length - 2, MIN_PADDLE_SIZE)
        self.img = [[(Back.BLUE + ' ' + Back.RESET)
                     for _ in range(self.length)]]
