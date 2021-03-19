import globals
from globals import powerup_move_interval, HEIGHT, WIDTH
import time
from colorama import Fore


class PowerUp():
    '''Base class for a powerup'''

    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel
        self.last_move_time = time.time()
        self.activated_time = time.time()
        self.destroyed = False
        self.activated = False

    def move(self):
        if time.time() - self.last_move_time > powerup_move_interval:
            if (self.pos[0] + self.vel[0] >= WIDTH - 1) or (self.pos[0] + self.vel[0] < 1):
                self.vel[0] *= -1
            self.pos[0] += self.vel[0]

            #self.vel[1] += 1    # gravity
            if (self.pos[1] + self.vel[1] < 1):
                self.vel[1] *= -1
            if self.pos[1] + 1 >= HEIGHT:
                self.destroyed = True
            self.pos[1] += self.vel[1]

            self.last_move_time = time.time()
    
    def unmove(self):
        # Move one step back. Used for collision handling with brick
        self.pos[0] -= self.vel[0]
        self.pos[1] -= self.vel[1]
    
    def bounce_on(self, obj):
        # Change direction on collision with brick

        if type(obj).__name__ == 'Brick':
            self.unmove()
            # Sideways collision
            if self.pos[0] < obj.pos[0] or self.pos[0] > obj.pos[0] + obj.length - 1:
                self.vel[0] *= -1
            # Top/Bottom collision
            else:
                self.vel[1] *= -1
            self.move()


class ExpandPaddle(PowerUp):
    '''Class for the expand paddle powerup'''

    def __init__(self, pos, vel):
        super().__init__(pos, vel)
        self.img = [[Fore.CYAN + 'X' + Fore.RESET]]

    def activate(self, **kwargs):
        kwargs['paddle'].expand()
        self.activated = True
        self.activated_time = time.time()

    def deactivate(self, **kwargs):
        kwargs['paddle'].shrink()
        self.activated = False
        self.destroyed = True


class ShrinkPaddle(PowerUp):
    '''Class for the shrink paddle powerup'''

    def __init__(self, pos, vel):
        super().__init__(pos, vel)
        self.img = [[Fore.RED + '~' + Fore.RESET]]

    def activate(self, **kwargs):
        kwargs['paddle'].shrink()
        self.activated = True
        self.activated_time = time.time()

    def deactivate(self, **kwargs):
        kwargs['paddle'].expand()
        self.activated = False
        self.destroyed = True


class MultiBalls(PowerUp):
    '''Class for the multiballs powerup'''

    def __init__(self, pos, vel):
        super().__init__(pos, vel)
        self.img = [[Fore.GREEN + '*' + Fore.RESET]]

    def double_balls(self, balls):
        from ball import Ball
        new_balls = []
        for ball in balls:
            new_ball = Ball([ball.pos[0], ball.pos[1]], [-1, -1])
            new_ball.stuck = False
            new_ball.go_through_bricks = ball.go_through_bricks
            new_balls.append(new_ball)
        balls += new_balls

    def remove_balls(self, balls):
        while(len(balls) > 1):
            balls.pop()

    def activate(self, **kwargs):
        self.double_balls(kwargs['balls'])
        self.activated = True
        self.activated_time = time.time()

    def deactivate(self, **kwargs):
        self.remove_balls(kwargs['balls'])
        self.activated = False
        self.destroyed = True


class FastBall(PowerUp):
    '''Class for the fast blls powerup'''

    def __init__(self, pos, vel):
        super().__init__(pos, vel)
        self.img = [[Fore.MAGENTA + '>' + Fore.RESET]]

    def activate(self, **kwargs):
        globals.ball_move_interval = 0.05
        self.activated = True
        self.activated_time = time.time()

    def deactivate(self, **kwargs):
        globals.ball_move_interval = 0.1
        self.activated = False
        self.destroyed = True


class ThruBall(PowerUp):
    '''Class for the thru blls powerup'''

    def __init__(self, pos, vel):
        super().__init__(pos, vel)
        self.img = [[Fore.BLUE + '^' + Fore.RESET]]

    def activate(self, **kwargs):
        for ball in kwargs['balls']:
            ball.go_through_bricks = True
        self.activated = True
        self.activated_time = time.time()

    def deactivate(self, **kwargs):
        for ball in kwargs['balls']:
            ball.go_through_bricks = False
        self.activated = False
        self.destroyed = True


class PaddleGrab(PowerUp):
    '''Class for the paddle grab powerup'''

    def __init__(self, pos, vel):
        super().__init__(pos, vel)
        self.img = [[Fore.GREEN + '#' + Fore.RESET]]

    def activate(self, **kwargs):
        kwargs['paddle'].grab = True
        self.activated = True
        self.activated_time = time.time()

    def deactivate(self, **kwargs):
        kwargs['paddle'].grab = False
        self.activated = False
        self.destroyed = True


class ShootingPaddle(PowerUp):
    '''Class for the shooting paddle powerup'''

    def __init__(self, pos, vel):
        super().__init__(pos, vel)
        self.img = [[Fore.RED + 'T' + Fore.RESET]]

    def activate(self, **kwargs):
        kwargs['paddle'].activate_shooting()
        self.activated = True
        self.activated_time = time.time()

    def deactivate(self, **kwargs):
        kwargs['paddle'].deactivate_shooting()
        self.activated = False
        self.destroyed = True