from globals import WIDTH


class Paddle():
    '''Class for the paddle'''

    def __init__(self, pos):
        self.length = 7
        self.img = [['#' for _ in range(self.length)]]
        self.pos = pos
        self.speed = 2

    def move(self, dir):
        old_x = self.pos[0]
        if dir == "d":
            if (self.pos[0] + self.length + 1 < WIDTH):
                self.pos[0] += self.speed
        elif dir == "a":
            if (self.pos[0] > 1):
                self.pos[0] -= self.speed

        return self.pos[0] - old_x
