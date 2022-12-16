import enum
import itertools

import numpy as np

from tools import numpy_tools

rock_lines: list[list[tuple[int, int]]] = []
with open("input.txt", "r") as f:
    for line in f:
        line = line.rstrip()
        coords = line.split(' -> ')
        rock = []
        for pair in coords:
            num = [
                int(_)
                for _ in pair.split(',')
            ]
            assert len(num) == 2
            rock.append((num[0], num[1]))
        rock_lines.append(rock)


class Material(enum.Enum):
    Rock = enum.auto()
    Sand = enum.auto()
    Air = enum.auto()


def render_grid(rock_lines: list[list[tuple[int, int]]]) -> np.ndarray:
    # x increases to the right; y increases toward down
    min_x = min_y = max_x = max_y = None
    for rock_line in rock_lines:
        for coord in rock_line:
            if min_x is None or min_x > coord[0]:
                min_x = coord[0]
            if max_x is None or max_x < coord[0]:
                max_x = coord[0]
            if min_y is None or min_y > coord[1]:
                min_y = coord[1]
            if max_y is None or max_y < coord[1]:
                max_y = coord[1]

    print(f"Cave system spans from x=[{min_x},{max_x}] y=[{min_y},{max_y}]")
    assert min_x >= 0
    assert min_y >= 0
    grid = np.full(shape=(max_x + 1, max_y + 1), dtype='<U1', fill_value='.')

    for rock_line in rock_lines:
        for rock_from, rock_to in itertools.pairwise(rock_line):
            if rock_from[0] != rock_to[0]:  # horizontal
                assert rock_from[1] == rock_to[1]
                min_x = min(rock_from[0], rock_to[0])
                max_x = max(rock_from[0], rock_to[0])
                grid[min_x:(max_x+1), rock_from[1]] = 'R'
            elif rock_from[1] != rock_to[1]:  # vertical
                assert rock_from[0] == rock_to[0]
                min_y = min(rock_from[1], rock_to[1])
                max_y = max(rock_from[1], rock_to[1])
                grid[rock_from[0], min_y:(max_y+1)] = 'R'
            else:
                raise ValueError("huh?")
    return grid


cave = render_grid(rock_lines)
sand_source = (500, 0)
bottom_most_rock_y = cave.shape[1]

# add a bit more space to avoid bounds-checks in the loop
cave = np.concatenate([cave, np.full(shape=(cave.shape[0], 1), fill_value='.')], axis=1)
#print(numpy_tools.str_values_only(cave.T))

sand_pos = None
units_of_sand_came_to_rest = 0
while True:
    if sand_pos is None:
        sand_pos = sand_source
    if sand_pos[1] >= bottom_most_rock_y:
        break

    sand_next_candidates = [
        (sand_pos[0], sand_pos[1]+1),  # first try to move down
        (sand_pos[0]-1, sand_pos[1]+1),  # try down-left
        (sand_pos[0]+1, sand_pos[1]+1),  # try down-right
    ]
    for c in sand_next_candidates:
        if cave[c] == '.':
            sand_pos = c
            break
    else:  # come to rest
        cave[sand_pos] = 'o'
        sand_pos = None
        units_of_sand_came_to_rest += 1

#print(numpy_tools.str_values_only(cave.T))
print(units_of_sand_came_to_rest)