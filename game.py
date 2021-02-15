import os
from input import Get, input_to
from paddle import Paddle
from ball import Ball
from grid import Grid
from globals import *
from utils import *

getinp = Get()


def game_loop():
    clear()
    grid = Grid()
    paddle = Paddle([WIDTH//2, 3 * HEIGHT//4])
    ball = Ball([paddle.pos[0] + paddle.length//2, paddle.pos[1] - 1])

    grid.draw(paddle)
    print(grid)

    while True:
        # Temporary grid for comparison
        tempGrid = Grid()

        # Input
        inp = input_to(getinp, 0.02)
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
        if (ball.pos[1] == paddle.pos[1]) and (paddle.pos[0] <= ball.pos[0] < paddle.pos[0] + paddle.length):
            ball.unmove()
            paddle_center = paddle.pos[0] + paddle.length//2
            if ball.pos[0] > paddle_center:
                ball.vel[0] = min(ball.vel[0] + 1, 2)
            elif ball.pos[0] < paddle_center:
                ball.vel[0] = max(ball.vel[0] - 1, -2)
            ball.vel[1] *= -1
            ball.move()

        # Drawing
        tempGrid.draw(paddle)
        tempGrid.draw(ball)

        # Check for grid update and print
        if grid != tempGrid:
            grid = tempGrid
            clear()
            print(grid)


if __name__ == '__main__':
    game_loop()
