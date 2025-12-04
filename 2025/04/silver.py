import numpy
import scipy.signal

grid = []
with open("input.txt") as f:
    for line in f.readlines():
        line = line.rstrip()
        line = [1 if ch == "@" else 0 for ch in line]
        grid.append(line)

grid = numpy.array(grid)
#print(grid)

kernel = numpy.array([[1, 1, 1],[1, 0, 1], [1, 1, 1]])
surrounding = scipy.signal.convolve2d(grid, kernel, mode="same", boundary="fill", fillvalue=0)

accessible_rolls = 0
it = numpy.nditer(grid, flags=['multi_index'])
for e in it:
    if e and surrounding[it.multi_index] < 4:
        accessible_rolls += 1

print(accessible_rolls)
