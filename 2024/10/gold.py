import numpy as np

with open("input.txt", "r") as f:
    height = [
        list(int(_) for _ in line.strip())
        for line in f.readlines()
    ]
height = np.array(height)

#print(height)


def find_next_positions(coord: tuple[int, int]) -> list[tuple[int, int]]:
    global height
    next_step: list[tuple[int, int]] = []
    if 0 < coord[0]:
        left = (coord[0] - 1, coord[1])
        if height[left] == height[coord] + 1:
            next_step.append(left)
    if 0 < coord[1]:
        up = (coord[0], coord[1] - 1)
        if height[up] == height[coord] + 1:
            next_step.append(up)
    if coord[0] < height.shape[0] - 1:
        right = (coord[0] + 1, coord[1])
        if height[right] == height[coord] + 1:
            next_step.append(right)
    if coord[1] < height.shape[1] - 1:
        down = (coord[0], coord[1] + 1)
        if height[down] == height[coord] + 1:
            next_step.append(down)
    return next_step


def walk_up(pos: tuple[int, int], _trail: list[tuple[int, int]]) -> tuple[int, set[tuple[int, int]]]:
    global height
    if height[pos] == 9:
        return 1, {pos}

    next_steps = find_next_positions(pos)
    num_paths: int = 0
    high_points: set[tuple[int, int]] = set()
    for path in next_steps:
        this_num_paths, this_path_high_points = walk_up(path, [*_trail, path])
        num_paths += this_num_paths
        high_points.update(this_path_high_points)
    return num_paths, high_points


starting_points = np.where(height == 0)
starting_points = [
    (int(coord[0]), int(coord[1]))
    for coord in np.array(starting_points).transpose()
]
#print(starting_points)
total_rating = 0
total_score = 0
for starting_point in starting_points:
    print(starting_point)
    traishead_rating, trailhead_score = walk_up(starting_point, [starting_point])
    print(f"starting at {starting_point} => score={trailhead_score}, rating={traishead_rating}")
    total_rating += traishead_rating
    total_score += len(trailhead_score)
print(f"{total_rating=}, {total_score=}")
