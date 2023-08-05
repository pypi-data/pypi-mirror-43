#!/usr/bin/python

import curses, argparse
from itertools import cycle

import numpy as np
from scipy.signal import convolve2d


def update(p, array, constants, height, width):

    alpha, beta, gamma = constants
    # Count the average amount of each species in the 9 cells around each cell
    q = (p + 1) % 2
    s = np.zeros((3, height, width))
    m = np.ones((3, 3)) / 9
    for k in range(3):
        s[k] = convolve2d(array[p, k], m, mode="same", boundary="wrap")
    # Apply the reaction equations
    array[q, 0] = s[0] + s[0] * (alpha * s[1] - gamma * s[2])
    array[q, 1] = s[1] + s[1] * (beta * s[2] - alpha * s[0])
    array[q, 2] = s[2] + s[2] * (gamma * s[0] - beta * s[1])
    # Ensure the species concentrations are kept within [0,1].
    np.clip(array[q], 0, 1, array[q])

    return array


def render(args):

    if args.reverse:
        args.color = args.color[::-1]

    screen = curses.initscr()
    args.size = screen.getmaxyx()
    height, width = args.size

    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, 0, 0)
    curses.init_pair(2, 1, 0)
    curses.init_pair(3, 3, 0)
    curses.init_pair(4, 4, 0)
    screen.clear

    # Initialize the array with random amounts of A, B and C.
    array = np.random.random(size=(2, 3, height, width))

    phase = cycle([0, 1])
    while True:
        p = next(phase)
        array = update(p, array, args.coefficients, *args.size)
        for line in range(height - 1):
            for column in range(width - 1):
                value = np.floor(array[p, 0, line, column] * 9.9).astype("int64")
                screen.addstr(
                    line,
                    column,
                    args.ascii[value],
                    curses.color_pair(args.color[value]) | curses.A_BOLD,
                )
        screen.refresh()
        screen.timeout(30)
        if screen.getch() != -1:
            break
    curses.endwin()


def main():

    # Default parameters
    coef = 1.0, 1.0, 1.0
    chars = (" ", ".", ".", ":", "*", "*", "*", "#", "#", "@")
    colors = (1, 1, 2, 2, 2, 3, 3, 3, 4, 4)

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--ascii",
        action="store",
        default=chars,
        nargs=10,
        help="10 ASCII characters to be use in the rendering",
    )
    parser.add_argument(
        "--color",
        action="store",
        default=colors,
        nargs=10,
        help="10 numbers (ranging from 0 to 9) to map colors to the ASCII character",
    )
    parser.add_argument(
        "--coefficients",
        action="store",
        default=coef,
        nargs=3,
        type=float,
        help="values from alpha, beta and gama (floats separeted by space)",
    )
    parser.add_argument(
        "--reverse", action="store_true", help="reverse colorsheme", default=False
    )

    args = parser.parse_args()

    render(args)


if __name__ == "__main__":
    main()
