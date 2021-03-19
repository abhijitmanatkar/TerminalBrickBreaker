from colorama import Fore
import time
from globals import LASER_MOVE_INTERVAL

class Laser():
    "Class for laser"

    def __init__(self, pos):
        self.pos = pos
        self.img = [[Fore.YELLOW + '|' + Fore.RESET]]
        self.speed = 1
        self.destroyed = False
        self.last_move_time = time.time()

    def move(self):
        if time.time() - self.last_move_time > LASER_MOVE_INTERVAL:
            self.pos[1] -= self.speed
            if (self.pos[1] < 1):
                self.destroyed = True
    