import os
from brick import Brick
from ball import Ball
from colorama import Fore, Back
from globals import WIDTH


def clear():
    os.system('tput reset')


def header(tm, score, lives):
    '''Display time, score, lives'''
    formatted_time = format_time(tm)
    time_string = "Time: " + formatted_time
    score_string = "Score: " + str(score)
    lives_string = "Lives: " + str(lives)
    empty_space_1 = " " * \
        (WIDTH // 2 - len(time_string) - len(lives_string)//2)
    empty_space_2 = " " * \
        (WIDTH // 2 - len(score_string) - len(lives_string)//2)
    empty_space_2 += " " * (WIDTH + 2 - len(time_string) - len(score_string) -
                            len(lives_string) - len(empty_space_1) - len(empty_space_2))
    score_string = Fore.BLACK + "Score: " + Fore.GREEN + str(score)
    time_string = Fore.BLACK + "Time: " + Fore.BLUE + formatted_time
    lives_string = Fore.BLACK + "Lives: " + Fore.RED + str(lives)
    head = Back.WHITE + time_string + empty_space_1 + lives_string + \
        empty_space_2 + score_string + Fore.RESET + Back.RESET
    return head


def format_time(tm):
    tm = int(tm)
    ret = ""
    if tm // 60 > 0:
        ret += str(tm // 60)
    else:
        ret += "0"
    ret += ":"
    if tm % 60 >= 10:
        ret += str(tm % 60)
    else:
        ret += "0" + str(tm % 60)

    return ret


def gen_bricks(level):
    bricks_pos = [[[5, 3, 4], [12, 3, 3], [19, 3, 3], [26, 3, 3], [33, 3, 3], [40, 3, 4], 
                  [5, 5, 3], [12, 5, 3], [19, 5, 3], [26, 5, 3], [33, 5, 3], [40, 5, 3],
                  [5, 7, 5], [12, 7, 2], [19, 7, 5], [26, 7, 2], [33, 7, 5], [40, 7, 2], 
                  [5, 9, 2], [12, 9, 5], [19, 9, 2], [26, 9, 5], [33, 9, 2], [40, 9, 5], 
                  [5, 11, 1], [12, 11, 1], [19, 11, 1], [26, 11, 1], [33, 11, 1], [40, 11, 1], 
                  [5, 13, 4], [12, 13, 1], [19, 13, 1], [26, 13, 1], [33, 13, 1], [40, 13, 4]],

                  [[5, 3, 4], [12, 3, 3], [19, 3, 3], [26, 3, 3], [33, 3, 3], [40, 3, 4], 
                  [5, 5, 3], [12, 5, 3], [19, 5, 3], [26, 5, 3], [33, 5, 3], [40, 5, 3],
                  [5, 7, 2], [12, 7, 2], [19, 7, 2], [26, 7, 2], [33, 7, 2], [40, 7, 2], 
                  [5, 9, 4], [12, 9, 4], [19, 9, 4], [26, 9, 4], [33, 9, 4], [40, 9, 4], 
                  [5, 11, 1], [12, 11, 1], [19, 11, 1], [26, 11, 1], [33, 11, 1], [40, 11, 1], 
                  [5, 13, 4], [12, 13, 1], [19, 13, 1], [26, 13, 1], [33, 13, 1], [40, 13, 4]],

                  [[5, 3, 4], [12, 3, 3], [19, 3, 3], [26, 3, 3], [33, 3, 3], [40, 3, 4], 
                  [5, 5, 3], [12, 5, 3], [19, 5, 3], [26, 5, 3], [33, 5, 3], [40, 5, 3],
                  [5, 7, 2], [12, 7, 2], [19, 7, 2], [26, 7, 2], [33, 7, 2], [40, 7, 2], 
                  [5, 9, 2], [12, 9, 2], [19, 9, 2], [26, 9, 2], [33, 9, 2], [40, 9, 2], 
                  [5, 11, 4], [12, 11, 4], [19, 11, 4], [26, 11, 4], [33, 11, 4], [40, 11, 4], 
                  [5, 13, 4], [12, 13, 1], [19, 13, 1], [26, 13, 1], [33, 13, 1], [40, 13, 4]]]

    # bricks_pos2 = [[5, 13, 4], [12, 13, 1], [19, 13, 1],
    #              [26, 13, 1], [33, 13, 1], [40, 13, 4]]
    #bricks_pos = [5, 12, 19, 26, 33, 40]
    bricks = []
    for brick in bricks_pos[level-1]:
        bricks.append(Brick([brick[0], brick[1]], brick[2]))
    '''
    for y in brick_y:
        for x in brick_x:
            bricks.append(Brick([x, y], strength=5-(y//2)))
    '''
    return bricks
