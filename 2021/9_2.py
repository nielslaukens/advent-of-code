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

# Locations of height 9 do not count as being in any basin, and all other locations will always be part of exactly one basin.
# => every basin will be separated by other basins with 9's,
# => otherwise we could get [0 1 0] and the 1 would be ambiguous to which basin it belongs
in_basin = numpy.where(height_map < 9, numpy.ones(height_map.shape), numpy.zeros(height_map.shape))


def flood_fill_size(is_inside: numpy.ndarray, pos) -> int:
    # https://en.wikipedia.org/wiki/Flood_fill
    if is_inside[pos[0], pos[1]] == 0:
        return 0

    is_inside[pos[0], pos[1]] = 0
    size = 1
    if pos[0] > 0:
        size += flood_fill_size(is_inside, [pos[0]-1, pos[1]])
    if pos[1] > 0:
        size += flood_fill_size(is_inside, [pos[0], pos[1]-1])
    if pos[0] < is_inside.shape[0]-1:
        size += flood_fill_size(is_inside, [pos[0]+1, pos[1]])
    if pos[1] < is_inside.shape[1]-1:
        size += flood_fill_size(is_inside, [pos[0], pos[1]+1])
    return size


basin_size = {}
for low_point in np.swapaxes(low_points, 0, 1):
    # find basin size
    basin_size[tuple(low_point.tolist())] = flood_fill_size(in_basin, low_point)

print("Basin sizes:")
print(basin_size)

largest_basins = sorted(basin_size.keys(), key=basin_size.get, reverse=True)
print("Basins, sorted by size:")
print(largest_basins)

result = basin_size[largest_basins[0]] * basin_size[largest_basins[1]] * basin_size[largest_basins[2]]
print(result)
