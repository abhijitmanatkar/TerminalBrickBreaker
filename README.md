# Terminal Brick Breaker

<i>Made by Abhijit Mantkar (2019101108)</i>

## Installation and running

Install colorama:

```bash
$ pip install colorama
```

Start by executing:

```bash
$ python main.py
```

<b>Note</b>: Python 3 is required for running the game.

## About the game

This is a clone of the classic Brick Breaker game for the terminal with some extra features.
The objective is to destroy bricks by smashing them with a bouncing ball in the shortest possible time without running out of lives. The ball is bounced off a paddle which the player can move left and right. A life is lost when the ball touches the ground below the paddle.

### Rules

- There are 3 levels in the game. The last level of the game has a boss enemy
- The player gets 3 lives. If the ball touches the ground below the paddle, the player loses a life. The game ends in a loss if the player loses all lives.
- The score is calculated as
  `score = 10 * number of bricks destroyed - 0.5 * time(in seconds)`
- Whenever a brick is destroyed, a powerup may appear with a certain probability. The effect of the powerup lasts for 20 seconds.
- Powerups include:
  - X - Increasing length of paddle
  - ~ - Decreasing length of paddle
  - \# - Making the ball stick to the paddle every time it is caught
  - \> - Increasing the speed of the ball
  - ^ - Through ball - Making the ball pass through every brick and destroying it
  - \* - Doubling the number of balls
  - T - Shoot lasers from paddle. Lasers affect bricks
- After a certain amount of time, the whole ensemble of bricks starts moving down towards the player on every ball touch. If the bricks reach the player, then it is game over.

### How to play

- <kbd>A</kbd>/<kbd>D</kbd> keys move the paddle left and right
- When a ball is stuck to the paddle, release by pressing <kbd>R</kbd>
- Quit the game at any time by pressing <kbd>Q</kbd>
- To shoot lasers, press <kbd>X</kbd>
- To skip a level, press <kbd>S</kbd>

## Features

### Bricks

- Bricks have 4 strength levels. The highest strength level is unbreakable.
- There is also a rainbow brick which changes strength levels continuosly.

### Boss

- The boss follows the players movements and drops bombs on the player every 5 seconds.
- The boss has a health which can be reduced by hitting it with the ball
- When the health reaches 3 or 1, the boss builds a wall of bricks to protect itself.
- When the health reaches 0, the boss dies.

This game is built using OOP concepts. Each entity in the game is an object instance of an underlying class.

- <b>Abstraction</b> is incorporated by creating functions with semantic names such as `bounce_on`, `move`, etc which hide away the implemetation details.
- As all entities are instances of some class which includes both the relevant data variables for the entity as well as methods acting on the entity, <b>encapsulation</b> is involved.
- <b>Inheritance</b> is showcased in the case of different powerup classes inheriting from a base powerup class.
- <b>Polymorphism</b> is seen in the case of different powerup classes having their own unique `activate` and `deactivate` functions. The `move` method is also defined on multiple classes but has a different functionality in each.
