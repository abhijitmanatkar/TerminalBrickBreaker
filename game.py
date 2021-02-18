import os
import random
import time
from input import Get, input_to
from ball import Ball
from paddle import Paddle
from grid import Grid
from powerup import ExpandPaddle, ShrinkPaddle, MultiBalls, FastBall, ThruBall, PaddleGrab
import globals
from globals import WIDTH, HEIGHT, POWERUP_PROBABILITY, POWERUP_ACTIVE_TIME
from utils import clear, gen_bricks, format_time, header

getinp = Get()

powerup_classes = [ExpandPaddle, ShrinkPaddle,
                   MultiBalls, FastBall, ThruBall, PaddleGrab]


def game_loop():
    clear()
    grid = Grid()

    bricks = gen_bricks()

    started = False
    start_time = time.time()
    lives = 3

    score = 0
    brick_score = 0

    won = False

    while lives > 0 and not won:

        paddle = Paddle([WIDTH//2, HEIGHT - 4])
        balls = [Ball([random.randint(paddle.pos[0], paddle.pos[0] +
                                      paddle.length - 1), paddle.pos[1] - 1])]
        falling_powerups = []
        active_powerups = []

        globals.ball_move_interval = 0.1

        while True:
            # Temporary grid for comparison
            tempGrid = Grid()

            # Input
            inp = input_to(getinp, 0.07)  # , 0.025)
            if inp == 'q':
                clear()
                quit()
            elif inp in ['a', 'd']:
                delta_x = paddle.move(inp)
                for ball in balls:
                    if ball.stuck:
                        ball.drag(delta_x)
            elif inp == 'r':
                if not started:
                    started = True
                    start_time = time.time()
                for ball in balls:
                    ball.stuck = False
            elif inp == 'p':
                globals.ball_move_interval = 0.05

            # Updates
            for ball in balls:
                if not ball.stuck:
                    ball.move()
            balls = [ball for ball in balls if not ball.destroyed]
            if len(balls) == 0:
                lives -= 1
                break

            for powerup in falling_powerups:
                powerup.move()
            falling_powerups = [
                powerup for powerup in falling_powerups if not powerup.destroyed]

            # Check for collisions
            # Collision of balls with paddle
            for ball in balls:
                if paddle.collides_with(ball):
                    if paddle.grab:
                        ball.stick_to(paddle)
                    else:
                        ball.bounce_on(paddle)

            # Collision of ball with bricks
            for ball in balls:
                for i in range(len(bricks)):
                    if bricks[i].collides_with(ball):
                        if not ball.go_through_bricks:
                            ball.bounce_on(bricks[i])
                            bricks[i].take_damage()
                        else:
                            bricks[i].destroyed = True
                        if bricks[i].destroyed:
                            # Update score
                            if bricks[i].strength == 4:
                                brick_score += 20
                            else:
                                brick_score += 10

                            # Generate powerup if destroyed
                            if random.random() < POWERUP_PROBABILITY:
                                falling_powerups.append(random.choice(
                                    powerup_classes)(bricks[i].pos))
                bricks = [brick for brick in bricks if not brick.destroyed]

            # Collision of paddle with powerup
            for powerup in falling_powerups:
                if paddle.collides_with(powerup):
                    powerup.activate(paddle=paddle, balls=balls)
                    active_powerups.append(powerup)
                    falling_powerups = [
                        powerup for powerup in falling_powerups if not powerup.activated]

            # Deactivating powerups
            for powerup in active_powerups:
                if time.time() - powerup.activated_time >= POWERUP_ACTIVE_TIME:
                    powerup.deactivate(paddle=paddle, balls=balls)
            active_powerups = [
                powerup for powerup in active_powerups if not powerup.destroyed]

            # Drawing
            for brick in bricks:
                tempGrid.draw(brick)
            for powerup in falling_powerups:
                tempGrid.draw(powerup)
            for ball in balls:
                tempGrid.draw(ball)
            tempGrid.draw(paddle)

            # Calculate score
            time_penalty = 0.5 * int(time.time() - start_time)
            score = brick_score - time_penalty

            # Print
            grid = tempGrid
            clear()
            if started:
                print(header(time.time() - start_time, score, lives))
                #print(format_time(time.time() - start_time))
            else:
                print(header(0, 0, lives))
            print(grid, end="")
            if not started:
                print("Press R to release the ball and start the game")
                print("Press W/A to move the paddle and Q to quit the game")

            # Check if game over
            if len(bricks) <= 4:
                won = True
                for brick in bricks:
                    if brick.strength < 4:
                        won = False
                        break
                if won:
                    break

    if not won:
        print("Game over. You lose :(")
    else:
        print("You win!!")
    print("Your score: " + str(score))


if __name__ == '__main__':
    game_loop()
