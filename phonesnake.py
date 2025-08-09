#!/usr/bin/env python3
import curses
import random
import time

# Snake settings
INITIAL_SNAKE_LENGTH = 5
SNAKE_CHAR = "█"
FOOD_CHAR = "●"
SPEED = 0.15  # seconds per move

# Nokia phone dimensions
PHONE_WIDTH = 30
PHONE_HEIGHT = 20

def draw_phone(stdscr):
    """Draw a Nokia-style phone with a screen for the game."""
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    # Center phone
    top = (h - PHONE_HEIGHT) // 2 - 2
    left = (w - PHONE_WIDTH) // 2 - 2

    # Draw phone outline
    for y in range(PHONE_HEIGHT + 4):
        for x in range(PHONE_WIDTH + 4):
            if y == 0 or y == PHONE_HEIGHT + 3:
                stdscr.addch(top + y, left + x, "#")
            elif x == 0 or x == PHONE_WIDTH + 3:
                stdscr.addch(top + y, left + x, "#")
            else:
                stdscr.addch(top + y, left + x, " ")

    # Draw phone screen border
    for y in range(PHONE_HEIGHT + 2):
        for x in range(PHONE_WIDTH + 2):
            if y == 0 or y == PHONE_HEIGHT + 1:
                stdscr.addch(top + y + 1, left + x + 1, "+")
            elif x == 0 or x == PHONE_WIDTH + 1:
                stdscr.addch(top + y + 1, left + x + 1, "+")
            else:
                stdscr.addch(top + y + 1, left + x + 1, " ")

    return top + 2, left + 2  # screen start position

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    screen_top, screen_left = draw_phone(stdscr)

    # Initial snake position
    sx = PHONE_WIDTH // 2
    sy = PHONE_HEIGHT // 2
    snake = [(sx - i, sy) for i in range(INITIAL_SNAKE_LENGTH)]
    direction = (1, 0)  # right

    # Food
    food = (random.randint(1, PHONE_WIDTH - 2), random.randint(1, PHONE_HEIGHT - 2))

    score = 0
    while True:
        # Draw food
        stdscr.addch(screen_top + food[1], screen_left + food[0], FOOD_CHAR)

        # Draw snake
        for x, y in snake:
            stdscr.addch(screen_top + y, screen_left + x, SNAKE_CHAR)

        # Input
        key = stdscr.getch()
        if key == curses.KEY_UP and direction != (0, 1):
            direction = (0, -1)
        elif key == curses.KEY_DOWN and direction != (0, -1):
            direction = (0, 1)
        elif key == curses.KEY_LEFT and direction != (1, 0):
            direction = (-1, 0)
        elif key == curses.KEY_RIGHT and direction != (-1, 0):
            direction = (1, 0)
        elif key == ord("q"):
            break

        # Move snake
        head_x, head_y = snake[0]
        new_head = ((head_x + direction[0]) % PHONE_WIDTH,
                    (head_y + direction[1]) % PHONE_HEIGHT)

        if new_head in snake:
            break  # Game over

        snake.insert(0, new_head)

        # Check food
        if new_head == food:
            score += 1
            food = (random.randint(1, PHONE_WIDTH - 2), random.randint(1, PHONE_HEIGHT - 2))
        else:
            tail_x, tail_y = snake.pop()
            stdscr.addch(screen_top + tail_y, screen_left + tail_x, " ")

        stdscr.addstr(1, 2, f"Score: {score}")
        stdscr.refresh()
        time.sleep(SPEED)

    stdscr.nodelay(0)
    stdscr.addstr(screen_top + PHONE_HEIGHT // 2, screen_left + 5, "GAME OVER!")
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
