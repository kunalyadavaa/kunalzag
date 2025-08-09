#!/usr/bin/env python3
import os, time

# Pixel map for "KUNAL" (5 rows tall)
# 1 = █ pixel, 0 = space
KUNAL_PIXELS = [
    "█   █ ████  █   █ █   █ ████ ",
    "█   █ █   █ ██  █ ██  █ █    ",
    "█   █ ████  █ █ █ █ █ █ █ ██ ",
    "█   █ █     █  ██ █  ██ █   █",
    " ███  █     █   █ █   █  ███ ",
]

# Convert to mutable world
world = [list(row) for row in KUNAL_PIXELS]

def render():
    os.system("clear")
    for row in world:
        print("".join(row))

if __name__ == "__main__":
    # Animation: gradually reveal KUNAL
    total_pixels = sum(row.count("█") for row in KUNAL_PIXELS)
    revealed = 0

    for y in range(len(world)):
        for x in range(len(world[0])):
            if world[y][x] == "█":
                world[y][x] = " "
                render()
                time.sleep(0.005)

    # Reveal effect
    for y in range(len(world)):
        for x in range(len(world[0])):
            if KUNAL_PIXELS[y][x] == "█":
                world[y][x] = "█"
                render()
                time.sleep(0.01)
