import os
from brick import Brick
from ball import Ball


def clear():
    os.system('tput reset')


def gen_bricks():
    bricks_pos = [[5, 3, 4], [12, 3, 3], [19, 3, 3],
                  [26, 3, 3], [33, 3, 3], [40, 3, 4], [
                  5, 5, 3], [12, 5, 3], [19, 5, 3],
                  [26, 5, 3], [33, 5, 3], [40, 5, 3], [
        5, 7, 2], [12, 7, 2], [19, 7, 2],
        [26, 7, 2], [33, 7, 2], [40, 7, 2], [
        5, 9, 2], [12, 9, 2], [19, 9, 2],
        [26, 9, 2], [33, 9, 2], [40, 9, 2], [
            5, 11, 1], [12, 11, 1], [19, 11, 1],
        [26, 11, 1], [33, 11, 1], [40, 11, 1], [
            5, 13, 4], [12, 13, 1], [19, 13, 1],
        [26, 13, 1], [33, 13, 1], [40, 13, 4]]
    #bricks_pos = [5, 12, 19, 26, 33, 40]
    bricks = []
    for brick in bricks_pos:
        bricks.append(Brick([brick[0], brick[1]], brick[2]))
    '''
    for y in brick_y:
        for x in brick_x:
            bricks.append(Brick([x, y], strength=5-(y//2)))
    '''
    return bricks
