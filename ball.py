from globals import WIDTH, HEIGHT, BALL_MOVE_INTERVAL
import time


class Ball():
    '''Class for the ball'''

    def __init__(self, pos, vel=[1, 1]):
        self.img = [['O']]
        self.pos = pos
        self.vel = vel
        self.stuck = True
        self.last_move_time = time.time()

    def drag(self, delta_x):
        # Used when ball is stuck
        self.pos[0] += delta_x

    def move(self, delta_x=0):
        # Ball movement when free
        if time.time() - self.last_move_time > BALL_MOVE_INTERVAL:
            if (self.pos[0] + self.vel[0] >= WIDTH - 1) or (self.pos[0] + self.vel[0] < 1):
                self.vel[0] *= -1
            self.pos[0] += self.vel[0]

            if (self.pos[1] + self.vel[1] >= HEIGHT - 1) or (self.pos[1] + self.vel[1] < 1):
                self.vel[1] *= -1
            self.pos[1] += self.vel[1]

            self.last_move_time = time.time()

    def unmove(self):
        # Move one step back. Used for collision handling with paddle
        self.pos[0] -= self.vel[0]
        self.pos[1] -= self.vel[1]
