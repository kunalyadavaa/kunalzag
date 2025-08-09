#!/usr/bin/env python3
import os
import time
import shutil
import random

# Snake display settings
SNAKE_CHAR = "█"
SNAKE_LENGTH = 10
SPEED = 0.05  # seconds per frame

# Get terminal size
def get_terminal_size():
    size = shutil.get_terminal_size(fallback=(80, 24))
    return size.columns, size.lines

def clear():
    os.system("cls" if os.name == "nt" else "clear")

if __name__ == "__main__":
    width, height = get_terminal_size()
    snake = [(x, 0) for x in range(SNAKE_LENGTH)]  # initial position
    direction = (1, 0)  # moving right

    while True:
        # Move snake
        head_x, head_y = snake[-1]
        new_x = (head_x + direction[0]) % width
        new_y = (head_y + direction[1]) % height
        snake.append((new_x, new_y))
        if len(snake) > SNAKE_LENGTH:
            snake.pop(0)

        # Randomly change direction
        if random.random() < 0.05:
            direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

        # Draw world
        grid = [[" " for _ in range(width)] for _ in range(height)]
        for x, y in snake:
            grid[y][x] = SNAKE_CHAR

        clear()
        for row in grid:
            print("".join(row))

        time.sleep(SPEED)

