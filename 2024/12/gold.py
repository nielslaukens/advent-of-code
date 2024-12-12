from tools.flood_fill import flood_fill, nested_array_func, adjacent_positions

with open("sample2.txt", "r") as f:
    garden = [
        list(line.strip())
        for line in f.readlines()
    ]

print(garden)


locations_to_check: set[tuple[int, int]] = set()
for y, row in enumerate(garden):
    for x, plant in enumerate(row):
        locations_to_check.add((x, y))

garden_ = garden
garden = nested_array_func(garden_)

regions: list[set[tuple[int, int]]] = []
location_to_region: dict[tuple[int, int], set[tuple[int, int]]] = {}
while len(locations_to_check) > 0:
    start_loc = locations_to_check.pop()
    region = flood_fill(garden, start_loc)
    regions.append(region)
    region_nr = len(regions)
    for loc in region:
        try:
            locations_to_check.remove(loc)
        except KeyError:
            assert loc == start_loc
        location_to_region[loc] = region_nr


def adjacent_positions_named(position: tuple[int, int]) -> dict[str, tuple[int, int]]:
    n = {}
    if 0 < position[0]:
        n['N'] = (position[0] - 1, position[1])
    if 0 < position[1]:
        n['W'] = (position[0], position[1]-1)
    if position[0]+1 < len(garden_):
        n['S'] = (position[0]+1, position[1])
    if position[1]+1 < len(garden_[0]):
        n['E'] = (position[0], position[1]+1)
    return n


def find_corner(locations: set[tuple[int, int]]) -> tuple[int, int]:
    p = next(iter(locations))
    while True:
        neighbours = set(adjacent_positions(p))
        neighbours.intersection_update(locations)
        adj = adjacent_positions_named(p)
        if 'N' in adj and adj['N'] in locations:
            p = adj['N']
        elif 'W' in adj and adj['W'] in locations:
            p = adj['W']
        else:
            return p


def one_step(loc: tuple[int, int], dir: str) -> tuple[int, int]:
    if dir == 'N':
        return (loc[0] - 1, loc[1])
    elif dir == 'E':
        return (loc[0], loc[1] + 1)
    elif dir == 'S':
        return (loc[0] + 1, loc[1])
    elif dir == 'W':
        return (loc[0], loc[1] - 1)
    else:
        raise ValueError()


def cw(dir: str) -> str:
    if dir == 'N':
        return 'E'
    elif dir == 'E':
        return 'S'
    elif dir == 'S':
        return 'W'
    elif dir == 'W':
        return 'N'


def ccw(dir: str) -> str:
    if dir == 'N':
        return 'W'
    elif dir == 'E':
        return 'N'
    elif dir == 'S':
        return 'E'
    elif dir == 'W':
        return 'S'


def num_sides(locations: set[tuple[int, int]]) -> int:
    assert len(locations) > 0
    start_corner = find_corner(locations)  # NW corner, start moving East
    dir = 'E'

    p_in = start_corner
    p_out = one_step(p_in, ccw(dir))  # may be outside garden
    assert p_out not in locations
    sides = 0

    while True:
        next_p_in = one_step(p_in, dir)
        next_p_out = one_step(next_p_in, ccw(dir))
        if next_p_in in locations and next_p_out not in locations:
            # we're still on the edge
            p_in = next_p_in
            p_out = next_p_out
        elif next_p_out in locations:  # we should have turned CCW around p_out
            p_in = next_p_in
            dir = ccw(dir)
            sides += 1
        elif next_p_in not in locations:  # we should have turned CW around p_in
            dir = cw(dir)
            sides += 1
        if p_in == start_corner and dir == 'E':
            break

    return sides


print("Regions:")
total_price = 0
for region in regions:
    random_pos = next(iter(region))
    sides = num_sides(region)
    area = len(region)
    price = sides * area
    print(f"region {garden(random_pos)} around "
          f"{random_pos}: "
          f"A={area} P={sides} "
          f"fence price: {price}")
    total_price += price

print(f"{total_price=}")
