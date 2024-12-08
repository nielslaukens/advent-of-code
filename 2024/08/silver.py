import itertools

antennas: dict[str, set[tuple[int, int]]] = {}
map_size: tuple[int, int] = None
with open("input.txt", "r") as f:
    for y, line in enumerate(f.readlines()):
        for x, ch in enumerate(line.strip()):
            if ch == '.':
                pass
            else:
                antennas.setdefault(ch, set())
                antennas[ch].add((x, y))

    map_size = (x+1, y+1)

print(map_size)
print(antennas)


def in_map(coords: tuple[int, int]) -> bool:
    return 0 <= coords[0] < map_size[0] \
        and 0 <= coords[1] < map_size[1]


def antinodes_(antenna1: tuple[int, int], antenna2: tuple[int, int]) -> set[tuple[int, int]]:
    d = (antenna2[0] - antenna1[0], antenna2[1] - antenna1[1])
    return {
        (antenna1[0] - d[0], antenna1[1] - d[1]),
        (antenna2[0] + d[0], antenna2[1] + d[1]),
    }


def antinodes(antenna1: tuple[int, int], antenna2: tuple[int, int]) -> set[tuple[int, int]]:
    return {
        node
        for node in antinodes_(antenna1, antenna2)
        if in_map(node)
    }


antinode_coords: set[tuple[int, int]] = set()
for frequency, antenna_locations in antennas.items():
    for antenna1, antenna2 in itertools.combinations(antenna_locations, 2):
        a = antinodes(antenna1, antenna2)
        antinode_coords.update(a)

print(antinode_coords)
print(len(antinode_coords))
