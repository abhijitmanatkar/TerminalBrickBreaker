import os
import random
import time
import colorama
from input import Get, input_to
from ball import Ball
from paddle import Paddle
from boss import Boss
from grid import Grid
from powerup import ExpandPaddle, ShrinkPaddle, MultiBalls, FastBall, ThruBall, PaddleGrab, ShootingPaddle
import globals
from globals import WIDTH, HEIGHT, POWERUP_PROBABILITY, POWERUP_ACTIVE_TIME, BRICK_FALL_DEADLINE, BOMB_DROP_INTERVAL
from utils import clear, gen_bricks, format_time, header

getinp = Get()

powerup_classes = [ShootingPaddle, ExpandPaddle, ShrinkPaddle, MultiBalls, FastBall, ThruBall, PaddleGrab]

colorama.init()

score = 0
brick_score = 0
time_penalty = 0
lives = 3

def game_loop(level):
    global score, brick_score, time_penalty, lives

    clear()
    grid = Grid()

    bricks = gen_bricks(level)

    started = False
    start_time = time.time()
    
    # Number of seconds since start, used for score calculation only
    secs = 0

    won = False

    boss = None
    if level == 3:
        boss = Boss([WIDTH//2, 1])

    while lives > 0 and not won:

        paddle = Paddle([WIDTH//2, HEIGHT - 4])
        balls = [Ball([random.randint(paddle.pos[0], paddle.pos[0] +
                                      paddle.length - 1), paddle.pos[1] - 1])]
        falling_powerups = []
        active_powerups = []
        lasers = []
        bombs = []

        globals.ball_move_interval = 0.1

        # Time left for shooting powerup
        shoot_activate_time = 0

        # Bomb drop time
        last_bomb_time = time.time()

        while True:
            # Temporary grid for comparison
            tempGrid = Grid()

            # Input
            inp = input_to(getinp, 0.07)  # , 0.025)
            if inp == 'q':
                clear()
                quit()
            elif inp == 's':
                # Skipping level
                won = True
            elif inp in ['a', 'd']:
                delta_x = paddle.move(inp)
                for ball in balls:
                    if ball.stuck:
                        ball.drag(delta_x)
                if boss != None:
                    boss.move(inp)
            elif inp == 'r':
                if not started:
                    started = True
                    start_time = time.time()
                for ball in balls:
                    ball.stuck = False
            elif inp == 'p':
                globals.ball_move_interval = 0.05
            elif inp == 'x':
                laser_pair = paddle.shoot()
                if (laser_pair):
                    lasers.append(laser_pair[0])
                    lasers.append(laser_pair[1])

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

            for brick in bricks:
                if brick.rainbow:
                    brick.blink()

            for laser in lasers:
                laser.move()
            lasers = [laser for laser in lasers if not laser.destroyed]

            if time.time() - last_bomb_time > BOMB_DROP_INTERVAL:
                last_bomb_time = time.time()
                if boss:
                    bomb = boss.drop_bomb()
                    bombs.append(bomb)
            for bomb in bombs:
                bomb.move()
            bombs = [bomb for bomb in bombs if not bomb.destroyed]
            
            # Check for collisions
            # Collision of balls with paddle
            for ball in balls:
                if paddle.collides_with(ball):
                    if paddle.grab:
                        ball.stick_to(paddle)
                    else:
                        ball.bounce_on(paddle)
                    
                    # Falling bricks
                    if time.time() - start_time > BRICK_FALL_DEADLINE:
                        for brick in bricks:
                            brick.fall()
                            if brick.pos[1] >= paddle.pos[1]:
                                lives = 0
                                break
            
            # Check if bricks have reached paddle
            if lives == 0:
                break

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
                                    powerup_classes)(bricks[i].pos, [ball.vel[0], ball.vel[1]]))
                bricks = [brick for brick in bricks if not brick.destroyed]
            
            # Collision of powerup with bricks
            for powerup in falling_powerups:
                for i in range(len(bricks)):
                    if bricks[i].collides_with(powerup):
                        powerup.bounce_on(bricks[i])

            # Collision of brick with laser
            for laser in lasers:
                for i in range(len(bricks)):
                    if bricks[i].collides_with(laser):
                        bricks[i].take_damage()
                        laser.destroyed = True
                        if bricks[i].destroyed:
                            brick_score += 10
                            # Generate powerup if destroyed
                            if random.random() < POWERUP_PROBABILITY:
                                falling_powerups.append(random.choice(
                                    powerup_classes)(bricks[i].pos, [ball.vel[0], ball.vel[1]]))
                bricks = [brick for brick in bricks if not brick.destroyed]
            lasers = [laser for laser in lasers if not laser.destroyed]
                    
            # Collision of paddle with powerup
            for powerup in falling_powerups:
                if paddle.collides_with(powerup):
                    powerup.activate(paddle=paddle, balls=balls)
                    if type(powerup).__name__ == 'ShootingPaddle':
                        shoot_activate_time = time.time()
                    else:
                        active_powerups.append(powerup)
                    falling_powerups = [
                        powerup for powerup in falling_powerups if not powerup.activated]

            # Collision of paddle with bomb
            bomb_hit = False
            for bomb in bombs:
                if paddle.collides_with(bomb):
                    bomb_hit = True
                    break
            if bomb_hit:
                lives -= 1
                break

            # Boss collision with ball
            if boss:
                for ball in balls:
                    if boss.collides_with(ball):
                        boss.take_damage()
                        ball.bounce_on(boss)
                        if boss.health == 3 or boss.health == 1:
                            wall = boss.build_wall()
                            bricks += wall

                        if boss.destroyed:
                            boss = None

            # Deactivating powerups
            if time.time() - shoot_activate_time > POWERUP_ACTIVE_TIME:
                paddle.deactivate_shooting()
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
            for laser in lasers:
                tempGrid.draw(laser)
            if boss:
                tempGrid.draw(boss)
            for bomb in bombs:
                tempGrid.draw(bomb)
            tempGrid.draw(paddle)

            # Calculate score
            if started:
                if int(time.time() - start_time) > secs:
                    time_penalty += 0.5 #* int(time.time() - start_time)
                secs = int(time.time() - start_time)
                score = brick_score - time_penalty

            # Print
            grid = tempGrid
            clear()
            if started:
                print(header(time.time() - start_time, score, lives, level, time.time() - shoot_activate_time))
                #print(format_time(time.time() - start_time))
            else:
                print(header(0, score, lives, level, time.time() - shoot_activate_time))
            print(grid, end="")
            if not started:
                if level > 1:
                    print("You have cleared level " + str(level - 1) + "!")
                print("Press R to release the ball and start level " + str(level))
                print("Press A/D to move the paddle and Q to quit the game")

            # Check if game over
            bricks_over = True
            for brick in bricks:
                if brick.strength < 4:
                    bricks_over = False
                    break
            if bricks_over: won = True
            if won:
                break

    if not won:
        print("Game over. You lose :(")
        print("Your level: " + str(level) + "\nYour score: " + str(score))
        quit()
    elif level == 3:
        print("Game over. You Won!!")
        print("Your level: " + str(level) + "\nYour score: " + str(score))


if __name__ == '__main__':
    game_loop(1)
    game_loop(2)
    game_loop(3)
