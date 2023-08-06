#!/usr/bin/python

import curses, argparse
from itertools import cycle

import numpy as np
from scipy.signal import convolve2d


def update_array(p, array, coefficients, height, width):

    alpha, beta, gamma = coefficients
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

    args.ascii = np.array(args.ascii)

    screen = curses.initscr()
    height, width = screen.getmaxyx()

    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, 1, args.background)
    curses.init_pair(2, 2, args.background)
    curses.init_pair(3, 3, args.background)
    curses.init_pair(4, 4, args.background)
    curses.init_pair(5, 5, args.background)
    curses.init_pair(6, 6, args.background)
    curses.init_pair(7, 7, args.background)
    screen.clear

    # Initialize the array with random amounts of A, B and C.
    array = np.random.random(size=(2, 3, height, width))

    phase = cycle([0, 1])
    while True:
        p = next(phase)
        array = update_array(p, array, args.coefficients, height, width)
        if args.fast:
            values = np.floor(array[p, 0] * 9.9).astype('int8')
            for line in range(height - 1):
                screen.addstr(
                    line,
                    0,
                    ''.join(args.ascii[values[line]]),
                    curses.color_pair(7) | curses.A_BOLD,
                )
        else:
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
    coefficients = 1.0, 1.0, 1.0
    asciis = np.array((" ", " ", ".", ":", "*", "*", "#", "#", "@", "@"))
    colors = (1, 1, 2, 2, 2, 3, 3, 3, 7, 7)

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--ascii',
        action='store',
        default=asciis,
        nargs=10,
        help='10 ASCII characters to be use in the rendering. Each point in the screen has a value between 0 and 1, and each ASCII charecter used as an input represents a range of values (e.g. 0.0-0.1, 0.1-0.2 etc)',
    )
    parser.add_argument(
        '--color',
        action='store',
        default=colors,
        nargs=10,
        type=int,
        help='10 numbers in the [0-7] range to map colors to the ASCII characters. They are: 0:black, 1:red, 2:green, 3:yellow, 4:blue, 5:magenta, 6:cyan, and 7:white',
    )
    parser.add_argument(
        '--coefficients',
        action='store',
        default=coefficients,
        nargs=3,
        type=float,
        help="Values for alpha, beta and gamma -- changes the reaction's behaviour. Default is alpha=1.0, beta=1.0, gamma=1.0",
    )
    parser.add_argument(
        '--background',
        action='store',
        default=1,
        type=int,
        help='Background color [0-7]',
    )
    parser.add_argument(
        '--fast',
        action='store_true',
        default=False,
        help='One color mode, better for bigger screens',
    )

    args = parser.parse_args()

    render(args)


if __name__ == "__main__":
    main()
