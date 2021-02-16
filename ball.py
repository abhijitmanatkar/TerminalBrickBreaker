from globals import WIDTH, HEIGHT, ball_move_interval
import time
from colorama import Fore


class Ball():
    '''Class for the ball'''

    def __init__(self, pos, vel=[1, 1]):
        self.img = [[Fore.YELLOW + 'O' + Fore.RESET]]
        self.pos = pos
        self.vel = vel
        self.stuck = True
        self.last_move_time = time.time()
        self.destroyed = False

    def drag(self, delta_x):
        # Used when ball is stuck
        self.pos[0] += delta_x

    def move(self, delta_x=0):
        # Ball movement when free
        if time.time() - self.last_move_time > ball_move_interval:
            if (self.pos[0] + self.vel[0] >= WIDTH - 1) or (self.pos[0] + self.vel[0] < 1):
                self.vel[0] *= -1
            self.pos[0] += self.vel[0]

            if (self.pos[1] + self.vel[1] < 1):
                self.vel[1] *= -1
            if (self.pos[1] + self.vel[1] >= HEIGHT - 1):
                self.destroyed = True
            self.pos[1] += self.vel[1]

            self.last_move_time = time.time()

    def unmove(self):
        # Move one step back. Used for collision handling with paddle
        self.pos[0] -= self.vel[0]
        self.pos[1] -= self.vel[1]

    def bounce_on(self, obj):
        # Change direction on collision with paddle/brick

        if type(obj).__name__ == 'Paddle':
            # Only top/bottom collision
            self.unmove()
            center = obj.pos[0] + obj.length//2
            right_center = center + obj.length//4
            left_center = obj.length//4
            if self.pos[0] < left_center:
                self.vel[0] = max(self.vel[0] - 2, -2)
            elif left_center <= self.pos[0] < center:
                self.vel[0] = max(self.vel[0] - 1, -2)
            elif center < self.pos[0] < right_center:
                self.vel[0] = min(self.vel[0] + 1, 2)
            elif right_center <= self.pos[0]:
                self.vel[0] = min(self.vel[0] + 2, 2)
            self.vel[1] *= -1
            self.move()

        elif type(obj).__name__ == 'Brick':
            self.unmove()
            # Sideways collision
            if self.pos[0] < obj.pos[0] or self.pos[0] > obj.pos[0] + obj.length - 1:
                self.vel[0] *= -1
            # Top/Bottom collision
            else:
                self.vel[1] *= -1
            self.move()
