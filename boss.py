from colorama import Back, Fore
from globals import WIDTH, HEIGHT, BOMB_MOVE_INTERVAL
from brick import Brick
import time

class Bomb():
    '''Bomb class'''
    def __init__(self, pos):
        self.pos = pos
        self.img = [['B']]
        self.speed = 1
        self.destroyed = False
        self.last_move_time = time.time()
    
    def move(self):
        if time.time() - self.last_move_time > BOMB_MOVE_INTERVAL:
            self.pos[1] += self.speed
            if self.pos[1] > HEIGHT:
                self.destroyed = True
            self.last_move_time = time.time()

class Boss():
    '''Class for boss enemy'''

    def __init__(self, pos):
        self.pos = pos
        self.length = 5
        self.health = 5
        self.speed = 2
        self.img = [[Back.RED + 'X' + Back.RESET for _ in range(5)],
                    [Fore.GREEN + 'H' + Fore.RESET for _ in range(self.health)]]
        self.destroyed = False

    def update_image(self):
        self.img = [[Back.RED + 'X' + Back.RESET for _ in range(5)],
                    [Fore.GREEN + 'H' + Fore.RESET for _ in range(self.health)] + [' ' for _ in range(5 - self.health)]]

    def move(self, dir):
        old_x = self.pos[0]
        if dir == "d":
            if (self.pos[0] + self.length + 1 <= WIDTH):
                self.pos[0] += self.speed
        elif dir == "a":
            if (self.pos[0] > 1):
                self.pos[0] -= self.speed

        return self.pos[0] - old_x

    def drop_bomb(self): 
        b = Bomb([self.pos[0] + self.length//2, self.pos[1] + 2])
        return b

    def collides_with(self, obj):
        if type(obj).__name__ == 'Ball':
            if obj.pos[1] != self.pos[1] and obj.pos[1] != self.pos[1] + 1:
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

    def take_damage(self):
        self.health -= 1
        if self.health == 0:
            self.destroyed = True

        self.update_image()


    def build_wall(self):
        x = self.pos[0]
        y = self.pos[1]
        positions = [[5, y+2], [12, y+2], [19, y+2], [26, y+2], [33, y+2], [40, y+2]]
        wall = [Brick(position, 1) for position in positions]
        return wall
        


    