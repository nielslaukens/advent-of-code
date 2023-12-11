import numpy
import typing

from tools.numpy_tools import str_values_only

grid = []
with open("input.txt", "r") as f:
    for line in f:
        line = line.rstrip()
        grid.append(list(line))

grid = numpy.array(grid)
# grid coordinates are (row, col)
#print(str_values_only(grid))

# expand the universe
rows_that_need_doubling = []
for row_num in range(grid.shape[0]):
    row = grid[row_num, :]
    if all(row == "."):
        rows_that_need_doubling.append(row_num)
for row_num in reversed(rows_that_need_doubling):
    # iterate back to front, so the row numbers don't change
    grid = numpy.insert(grid, row_num, grid[row_num, :], axis=0)

cols_that_need_doubling = []
for col_num in range(grid.shape[1]):
    col = grid[:, col_num]
    if all(col == "."):
        cols_that_need_doubling.append(col_num)
for col_num in reversed(cols_that_need_doubling):
    # iterate back to front, so the row numbers don't change
    grid = numpy.insert(grid, col_num, grid[:, col_num], axis=1)

print(str_values_only(grid))

galaxy_coords = []
with numpy.nditer(grid, flags=['multi_index']) as it:
    for element in it:
        if element == "#":
            galaxy_coords.append(it.multi_index)
print(galaxy_coords)


def all_pairs_no_order(l: list) -> typing.Generator[tuple, None, None]:
    for i, li in enumerate(l):
        for j, lj in enumerate(l):
            if i < j:
                yield li, lj


def manhattan_distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(a[0]-b[0]) + abs(a[1] - b[1])


sum_of_distances = 0
for g1, g2 in all_pairs_no_order(galaxy_coords):
    d = manhattan_distance(g1, g2)
    print(f"{g1} <-> {g2} = {d}")
    sum_of_distances += d

print(sum_of_distances)
