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


def get(coord, one_outside=0, more_outside=1) -> int:
    # Make a virtual border of 1 wide returning 0,
    # return 1 outside to contain the fill flood
    for axis in range(3):
        if coord[axis] < -1:
            return more_outside
        if coord[axis] > scan.shape[axis]:
            return more_outside
    for axis in range(3):
        if coord[axis] < 0:
            return one_outside
        if coord[axis] == scan.shape[axis]:
            return one_outside
    return scan[coord[0], coord[1], coord[2]]


assert scan[0, 0, 0] == 0  # no rock at (0, 0, 0)
# start flood-filling from (0,0,0)
water = {(0, 0, 0)}
found_new = water
while len(found_new):
    found_new_previous_iteration = found_new
    found_new = set()
    for coord in found_new_previous_iteration:
        neighbours = [
            (coord[0], coord[1], coord[2] + 1),
            (coord[0], coord[1], coord[2] - 1),
            (coord[0] - 1, coord[1], coord[2]),
            (coord[0] + 1, coord[1], coord[2]),
            (coord[0], coord[1] + 1, coord[2]),
            (coord[0], coord[1] - 1, coord[2])
        ]
        for neighbour in neighbours:
            if get(neighbour) == 0 and neighbour not in water:
                found_new.add(neighbour)

    water = water.union(found_new)

# now flag these coords as water
for coord in water:
    keep = True
    for axis in range(3):
        if coord[axis] < 0:
            keep = False
        if coord[axis] >= scan.shape[axis]:
            keep = False
    if keep:
        scan[coord[0], coord[1], coord[2]] = 2
#print(scan)

total_surface_area = 0
for coord in coords:
    neighbours = [
        (coord[0], coord[1], coord[2] + 1),
        (coord[0], coord[1], coord[2] - 1),
        (coord[0] - 1, coord[1], coord[2]),
        (coord[0] + 1, coord[1], coord[2]),
        (coord[0], coord[1] + 1, coord[2]),
        (coord[0], coord[1] - 1, coord[2])
    ]
    surface_area = 6
    for neighbour in neighbours:
        stuff_at_neighbour = get(neighbour, one_outside=2, more_outside=2)
        if stuff_at_neighbour < 2:  # rock or pocket of air
            surface_area -= 1

    total_surface_area += surface_area

print(total_surface_area)
