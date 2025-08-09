#!/usr/bin/env python3
"""
nokia_snake.py

Retro Nokia-like phone art with an embedded playable Snake game (curses).
Run with: python3 nokia_snake.py
"""

import curses
import random
import time
import locale
locale.setlocale(locale.LC_ALL, '')

# Screen (phone display) size inside the phone art
SCREEN_W = 22
SCREEN_H = 12

# Game settings
INITIAL_SNAKE_LEN = 4
FRAME_DELAY = 0.10  # seconds per frame (lower = faster)
FOOD_CHAR = "●"
SNAKE_CHAR = "█"

# Draw a simple Nokia-like phone frame; positions are relative to top-left of phone window
PHONE_PAD = [
    "┌" + "─" * (SCREEN_W + 2) + "┐",  # top border of phone screen
    "│" + " " * (SCREEN_W + 2) + "│",
    "│" + " " * (SCREEN_W + 2) + "│",
    "│" + " " * (SCREEN_W + 2) + "│",
    "│" + " " * (SCREEN_W + 2) + "│",
    "│" + " " * (SCREEN_W + 2) + "│",
    "│" + " " * (SCREEN_W + 2) + "│",
    "│" + " " * (SCREEN_W + 2) + "│",
    "│" + " " * (SCREEN_W + 2) + "│",
    "│" + " " * (SCREEN_W + 2) + "│",
    "│" + " " * (SCREEN_W + 2) + "│",
    "│" + " " * (SCREEN_W + 2) + "│",
    "└" + "─" * (SCREEN_W + 2) + "┘",  # bottom border of phone screen
]

# Below the screen, draw a keypad block (static)
KEYPAD = [
    "     ____  ____  ____     ",
    "    | 1  || 2  || 3  |    ",
    "    |____||____||____|    ",
    "    | 4  || 5  || 6  |    ",
    "    |____||____||____|    ",
    "    | 7  || 8  || 9  |    ",
    "    |____||____||____|    ",
    "    | *  || 0  ||  # |    ",
    "    |____||____||____|    ",
]

def place_food(snake, w, h):
    """Place food inside screen area, not on the snake."""
    while True:
        fx = random.randrange(0, w)
        fy = random.randrange(0, h)
        if (fx, fy) not in snake:
            return fx, fy

def draw_phone(stdscr, top, left):
    """Draw static phone art (frame + keypad) at top,left."""
    # Draw header (brand-ish)
    stdscr.addstr(top - 2, left + (SCREEN_W // 2) - 3, "NOKIA", curses.A_BOLD)

    # Draw phone screen frame (PHONE_PAD)
    for i, row in enumerate(PHONE_PAD):
        stdscr.addstr(top + i, left, row)

    # Draw keypad under the screen
    pad_top = top + len(PHONE_PAD) + 1
    for i, row in enumerate(KEYPAD):
        stdscr.addstr(pad_top + i, left, row)

    # small footer text
    stdscr.addstr(pad_top + len(KEYPAD), left + 2, "Retro Snake — q to quit", curses.A_DIM)

def game_loop(stdscr):
    curses.curs_set(0)            # hide cursor
    stdscr.nodelay(True)         # make getch non-blocking
    stdscr.keypad(True)          # enable special keys
    stdscr.timeout(int(FRAME_DELAY * 1000))

    # center phone on the terminal
    term_h, term_w = stdscr.getmaxyx()
    phone_h = len(PHONE_PAD) + 1 + len(KEYPAD) + 1
    phone_w = max(len(PHONE_PAD[0]), len(KEYPAD[0]))
    top = max(2, (term_h - phone_h) // 2)
    left = max(2, (term_w - phone_w) // 2)

    # initial snake (centered inside screen area)
    sx = SCREEN_W // 2
    sy = SCREEN_H // 2
    snake = [(sx - i, sy) for i in range(INITIAL_SNAKE_LEN)][::-1]  # list of (x,y) tail->head
    direction = (1, 0)  # moving right
    score = 0

    food = place_food(snake, SCREEN_W, SCREEN_H)

    paused = False
    game_over = False

    while True:
        # draw static phone
        stdscr.erase()
        draw_phone(stdscr, top, left)

        # draw the screen background (inside the frame)
        screen_top = top + 1
        screen_left = left + 1
        for y in range(SCREEN_H):
            # each row inside the frame is SCREEN_W wide
            stdscr.addstr(screen_top + y, screen_left, " " * SCREEN_W, curses.color_pair(0))

        # draw borders inside frame (a small inner border to mimic LCD bezel)
        stdscr.addstr(screen_top - 1, screen_left - 1, "┌" + "─" * SCREEN_W + "┐")
        for y in range(SCREEN_H):
            stdscr.addstr(screen_top + y, screen_left - 1, "│")
            stdscr.addstr(screen_top + y, screen_left + SCREEN_W, "│")
        stdscr.addstr(screen_top + SCREEN_H, screen_left - 1, "└" + "─" * SCREEN_W + "┘")

        # draw food
        fx, fy = food
        stdscr.addstr(screen_top + fy, screen_left + fx, FOOD_CHAR)

        # draw snake
        for i, (x, y) in enumerate(snake):
            ch = SNAKE_CHAR if i == len(snake) - 1 else SNAKE_CHAR
            stdscr.addstr(screen_top + y, screen_left + x, ch)

        # draw score / status
        status = f" Score: {score} "
        stdscr.addstr(screen_top - 2, left + 2, status, curses.A_REVERSE)

        if paused:
            stdscr.addstr(screen_top + SCREEN_H // 2, screen_left + (SCREEN_W // 2 - 3), " PAUSED ", curses.A_BOLD)
        if game_over:
            stdscr.addstr(screen_top + SCREEN_H // 2 - 1, screen_left + (SCREEN_W // 2 - 5), " GAME OVER ", curses.A_BLINK)
            stdscr.addstr(screen_top + SCREEN_H // 2, screen_left + (SCREEN_W // 2 - 9), " Press 'r' to restart ", curses.A_BOLD)

        stdscr.refresh()

        # input handling
        try:
            key = stdscr.getch()
        except KeyboardInterrupt:
            break

        if key != -1:
            if key in (curses.KEY_UP, ord('w'), ord('W')):
                if direction != (0, 1):
                    direction = (0, -1)
            elif key in (curses.KEY_DOWN, ord('s'), ord('S')):
                if direction != (0, -1):
                    direction = (0, 1)
            elif key in (curses.KEY_LEFT, ord('a'), ord('A')):
                if direction != (1, 0):
                    direction = (-1, 0)
            elif key in (curses.KEY_RIGHT, ord('d'), ord('D')):
                if direction != (-1, 0):
                    direction = (1, 0)
            elif key in (ord('p'), ord('P')):
                paused = not paused
            elif key in (ord('q'), ord('Q')):
                break
            elif key in (ord('r'), ord('R')) and game_over:
                # restart
                snake = [(sx - i, sy) for i in range(INITIAL_SNAKE_LENGTH)]
