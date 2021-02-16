import os
from input import Get, input_to
from ball import Ball
from paddle import Paddle
from grid import Grid
from globals import *
from utils import *

getinp = Get()


def game_loop():
    clear()
    grid = Grid()
    paddle = Paddle([WIDTH//2, HEIGHT - 4])
    ball = Ball([paddle.pos[0] + paddle.length//2, paddle.pos[1] - 1])
    bricks = gen_bricks()

    while True:
        # Temporary grid for comparison
        tempGrid = Grid()

        # Input
        inp = input_to(getinp, 0.025)
        if inp == 'q':
            clear()
            quit()
        if inp in ['a', 'd']:
            delta_x = paddle.move(inp)
            if ball.stuck:
                ball.drag(delta_x)
        if inp == 'r':
            ball.stuck = False

        # Updates
        if not ball.stuck:
            ball.move()

        # Check for collisions
        # Collision with paddle
        if paddle.collides_with(ball):
            ball.bounce_on(paddle)

        # Collision with bricks
        for i in range(len(bricks)):
            if bricks[i].collides_with(ball):
                ball.bounce_on(bricks[i])
                bricks[i].take_damage()
        bricks = [brick for brick in bricks if not brick.destroyed]

        # Drawing
        for brick in bricks:
            tempGrid.draw(brick)
        tempGrid.draw(paddle)
        tempGrid.draw(ball)

        # Check for grid update and print
        if grid != tempGrid:
            grid = tempGrid
            clear()
            print(grid)


if __name__ == '__main__':
    game_loop()
