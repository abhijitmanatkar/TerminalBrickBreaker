import os
from brick import Brick


def clear():
    os.system('tput reset')


def gen_bricks():
    brick_x = [4, 10, 16, 22, 28, 34, 40]
    brick_y = [2, 4, 6, 8]
    bricks = []
    for y in brick_y:
        for x in brick_x:
            bricks.append(Brick([x, y], strength=5-(y//2)))
    return bricks
