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

cols_that_need_doubling = []
for col_num in range(grid.shape[1]):
    col = grid[:, col_num]
    if all(col == "."):
        cols_that_need_doubling.append(col_num)

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


def manhattan_distance_with_doubling(a: tuple[int, int], b: tuple[int, int]) -> int:
    d = abs(a[0]-b[0]) + abs(a[1] - b[1])
    for row_num in rows_that_need_doubling:
        assert a[0] != row_num
        assert b[0] != row_num
        if min(a[0], b[0]) < row_num < max(a[0], b[0]):
            d += 1_000_000-1
    for col_num in cols_that_need_doubling:
        assert a[1] != col_num
        assert b[1] != col_num
        if min(a[1], b[1]) < col_num < max(a[1], b[1]):
            d += 1_000_000-1
    return d


sum_of_distances = 0
for g1, g2 in all_pairs_no_order(galaxy_coords):
    d = manhattan_distance_with_doubling(g1, g2)
    print(f"{g1} <-> {g2} = {d}")
    sum_of_distances += d

print(sum_of_distances)
