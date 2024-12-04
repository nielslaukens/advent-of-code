import numpy as np

from tools.numpy_tools import one_d_line

XMAS = "XMAS"

with open("input.txt", "r") as f:
    lines = [
        list(line.rstrip())
        for line in f.readlines()
    ]
    grid = np.array(lines)

print(grid)


def np_to_str(arr: np.ndarray) -> str:
    return ''.join(arr)


def find_xmas(x: int, y: int) -> int:
    if grid[y, x] != 'X':
        return 0

    directions = [
        (0, 1),  # horizontal
        (0, -1),  # horizontal, backwards
        (1, 0),  # vertical downward
        (-1, 0),  # vertical upward
        (1, 1),  # diagonally right-downward
        (-1, 1),  # diagonally right-upward
        (1, -1),  # diagonally left-down
        (-1, -1),  # diagonally left-up
    ]
    words = [
        one_d_line(grid, (y, x), len(XMAS), d)
        for d in directions
    ]
    words = [
        np_to_str(w)
        for w in words
        if w is not None
    ]
    xmases = 0
    for w in words:
        if w == XMAS:
            xmases += 1

    return xmases


xmases = 0
for x in range(grid.shape[1]):
    for y in range(grid.shape[0]):
        xmases += find_xmas(x, y)

print(xmases)
