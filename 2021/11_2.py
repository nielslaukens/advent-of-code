import re

import numpy
import scipy.ndimage


with open("11.input.txt", "r") as f:
    lines = []
    for line in f.readlines():
        lines.append([
            int(char)
            for char in line.strip()
        ])
    grid = numpy.array(lines)


def do_step(grid):
    new_grid = grid + 1

    def do_flash(neighbours):
        return sum(neighbours)

    flash_energy_drainer = numpy.ones(shape=grid.shape, dtype=int)
    while True:
        flash = new_grid > 9
        if not flash.any():
            break
        flash_energy_drainer *= (1 - flash)
        flash_boost = scipy.ndimage.generic_filter(
            input=flash,
            footprint=numpy.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]]),
            mode='constant', cval=0,
            function=do_flash,
            output=int,
        )
        new_grid = (new_grid + flash_boost) * flash_energy_drainer

    flashed = flash_energy_drainer == 0
    return new_grid, flashed


def highlight(s: str) -> str:
    return f'\033[91m{s}\033[0m'


def highlight_zeros(s: str) -> str:
    return re.sub(r'\b0\b', highlight('0'), s)


print("Initial situation:")
print(grid)
total_flashes = 0
step = 0
while True:
    step = step + 1
    print("")
    grid, flashed = do_step(grid)
    num_flashes = numpy.sum(flashed)
    print(f"After step {step} ({num_flashes} flashes this step):")
    print(highlight_zeros(str(grid)))
    total_flashes += num_flashes
    if num_flashes == 100:
        break
