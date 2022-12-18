import math

import numpy as np

coords = []
min_x = min_y = min_z = math.inf
max_x = max_y = max_z = -math.inf
with open("input.txt", "r") as f:
    for line in f:
        coord = [int(_) for _ in line.rstrip().split(',')]
        coords.append(coord)
        min_x = min(min_x, coord[0])
        min_y = min(min_y, coord[1])
        min_z = min(min_z, coord[2])
        max_x = max(max_x, coord[0])
        max_y = max(max_y, coord[1])
        max_z = max(max_z, coord[2])

print(min_x, min_y, min_z)
print(max_x, max_y, max_z)
scan = np.zeros(shape=(max_x+1, max_y+1, max_z+1), dtype=int)
for coord in coords:
    scan[coord[0], coord[1], coord[2]] = 1


def get(coord) -> int:
    for axis in range(3):
        if coord[axis] < 0:
            return 0
        if coord[axis] >= scan.shape[axis]:
            return 0
    return scan[coord[0], coord[1], coord[2]]


total_surface_area = 0
for coord in coords:
    above = get((coord[0], coord[1], coord[2]+1))
    below = get((coord[0], coord[1], coord[2]-1))
    left = get((coord[0]-1, coord[1], coord[2]))
    right = get((coord[0]+1, coord[1], coord[2]))
    before = get((coord[0], coord[1]+1, coord[2]))
    after = get((coord[0], coord[1]-1, coord[2]))

    surface_area = 6 - above - below - left - right - before - after
    total_surface_area += surface_area

print(total_surface_area)
