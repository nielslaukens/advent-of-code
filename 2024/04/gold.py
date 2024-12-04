import numpy as np

from tools.numpy_tools import one_d_line

MAS = "MAS"

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
    if grid[y, x] != 'A':
        return 0

    directions = [
        (1, 1),  # diagonally right-downward
        (-1, 1),  # diagonally right-upward
        (1, -1),  # diagonally left-down
        (-1, -1),  # diagonally left-up
    ]
    words = [
        one_d_line(grid, (y, x), len(MAS), d, start_offset=-1)
        for d in directions
    ]
    words = [
        np_to_str(w)
        for w in words
        if w is not None
    ]
    mases = sum([
        w == "MAS"
        for w in words
    ])
    # mases will either be 0, 1 or 2.
    # we can't double-count, since MAS is not symetrical

    return 1 if (mases == 2) else 0


xmases = 0
for x in range(grid.shape[1]):
    for y in range(grid.shape[0]):
        xmases += find_xmas(x, y)

print(xmases)
