import numpy

maps = [[]]
with open("sample.txt", "r") as f:
    for line in f:
        line = line.rstrip()
        if line == "":
            maps.append([])
        else:
            maps[-1].append(list(line))

maps = [numpy.array(_) for _ in maps]
print(maps[0])


def find_reflection(map: numpy.ndarray, axis: int):
    for i in range(1, map.shape[axis]):



for map in maps:
    _ = find_reflection(map, 1)
    print(_)
