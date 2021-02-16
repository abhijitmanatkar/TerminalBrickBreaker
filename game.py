import os
import random
from input import Get, input_to
from ball import Ball
from paddle import Paddle
from grid import Grid
from powerup import ExpandPaddle, ShrinkPaddle, MultiBalls
from globals import WIDTH, HEIGHT, POWERUP_PROBABILITY
from utils import clear, gen_bricks

getinp = Get()

powerup_classes = [ExpandPaddle, ShrinkPaddle, MultiBalls]


def game_loop():
    debug_string = ""
    clear()
    grid = Grid()
    paddle = Paddle([WIDTH//2, HEIGHT - 4])
    balls = [Ball([random.randint(paddle.pos[0], paddle.pos[0] +
                                  paddle.length - 1), paddle.pos[1] - 1])]
    bricks = gen_bricks()
    falling_powerups = []

    while True:
        debug_string = str(len(balls))
        # Temporary grid for comparison
        tempGrid = Grid()

        # Input
        inp = input_to(getinp, 0.025)
        if inp == 'q':
            clear()
            quit()
        elif inp in ['a', 'd']:
            delta_x = paddle.move(inp)
            for ball in balls:
                if ball.stuck:
                    ball.drag(delta_x)
        elif inp == 'r':
            for ball in balls:
                ball.stuck = False

        # Updates
        for ball in balls:
            if not ball.stuck:
                ball.move()
        balls = [ball for ball in balls if not ball.destroyed]

        for powerup in falling_powerups:
            powerup.move()
        falling_powerups = [
            powerup for powerup in falling_powerups if not powerup.destroyed]

        # Check for collisions
        # Collision of balls with paddle
        for ball in balls:
            if paddle.collides_with(ball):
                ball.bounce_on(paddle)

        # Collision of ball with bricks
        for ball in balls:
            for i in range(len(bricks)):
                if bricks[i].collides_with(ball):
                    ball.bounce_on(bricks[i])
                    bricks[i].take_damage()
                    if bricks[i].destroyed:
                        # Generate powerup if destroyed
                        if random.random() < POWERUP_PROBABILITY:
                            falling_powerups.append(random.choice(
                                powerup_classes)(bricks[i].pos))
            bricks = [brick for brick in bricks if not brick.destroyed]

        # Collision of paddle with powerup
        for powerup in falling_powerups:
            if paddle.collides_with(powerup):
                powerup.activate(paddle=paddle, balls=balls)

        # Drawing
        for brick in bricks:
            tempGrid.draw(brick)
        for powerup in falling_powerups:
            tempGrid.draw(powerup)
        for ball in balls:
            tempGrid.draw(ball)
        tempGrid.draw(paddle)

        # Check for grid update and print
        if grid != tempGrid:
            grid = tempGrid
            clear()
            print(debug_string)
            print(grid)


if __name__ == '__main__':
    game_loop()
