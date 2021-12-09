import numpy
import numpy as np
import scipy.ndimage

height_map = []
with open("9_1.input.txt", "r") as f:
    for line in f.readlines():
        line = line.strip()
        elements = [int(_) for _ in line]
        height_map.append(elements)

height_map = numpy.array(height_map)
print("Height map:")
print(height_map)


def is_local_minimum(neighbours):
    me = neighbours[2]
    return neighbours[0] > me and \
        neighbours[1] > me and \
        neighbours[3] > me and \
        neighbours[4] > me

# Note: scipy.ndimage.minimum_filter() == height_map does NOT work:
# this will also identify local flats
is_minima = scipy.ndimage.generic_filter(
    height_map,
    footprint=numpy.array([
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0],
    ]),
    mode='mirror',  # if (0, 0) < (1, 0), it's safe to mirror that to (-1, 0)
    function=is_local_minimum,
)
print("Minimum?")
print(is_minima)

low_points = numpy.nonzero(is_minima)
print(f"Low points: {np.swapaxes(low_points, 0, 1)}")
height_of_low_points = height_map[low_points]
print(f"Height of low point: {height_of_low_points}")
total_risk = 0
for height in height_of_low_points:
    rist_level = height + 1
    total_risk += rist_level

print(total_risk)
