import numpy
import scipy.signal

grid = []
with open("input.txt") as f:
    for line in f.readlines():
        line = line.rstrip()
        line = [1 if ch == "@" else 0 for ch in line]
        grid.append(line)

grid = numpy.array(grid)
print(grid)

kernel = numpy.array([[1, 1, 1],[1, 0, 1], [1, 1, 1]])

total_removed = 0
removed_some = True  # bootstrap
while removed_some:
    removed_some = False
    surrounding = scipy.signal.convolve2d(grid, kernel, mode="same", boundary="fill", fillvalue=0)

    new_grid = numpy.zeros(grid.shape)
    it = numpy.nditer(grid, flags=['multi_index'])
    for e in it:
        new_grid[it.multi_index] = e
        if e and surrounding[it.multi_index] < 4:
            new_grid[it.multi_index] = 0
            removed_some = True
            total_removed += 1

    print(new_grid)
    grid = new_grid

print(total_removed)
