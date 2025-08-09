#!/usr/bin/env python3
import os, time

# "KUNAL" pixel map (█ = filled, space = empty)
KUNAL = [
    "█   █ ████  █   █ █   █ ████ ",
    "█   █ █   █ ██  █ ██  █ █    ",
    "█   █ ████  █ █ █ █ █ █ █ ██ ",
    "█   █ █     █  ██ █  ██ █   █",
    " ███  █     █   █ █   █  ███ ",
]

def render(display):
    os.system("clear")
    for row in display:
        print("".join(row))

def zigzag_draw(name_pixels):
    height = len(name_pixels)
    width = len(name_pixels[0])
    display = [[" " for _ in range(width)] for _ in range(height)]

    # Zigzag traversal
    for y in range(height):
        if y % 2 == 0:  # left to right
            x_range = range(width)
        else:           # right to left
            x_range = range(width - 1, -1, -1)

        for x in x_range:
            if name_pixels[y][x] == "█":
                display[y][x] = "█"
            render(display)
            time.sleep(0.01)  # speed

if __name__ == "__main__":
    pixels = [list(row) for row in KUNAL]
    while True:
        zigzag_draw(pixels)
        time.sleep(0.5)  # pause before repeating
