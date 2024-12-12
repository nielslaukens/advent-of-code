from tools.flood_fill import flood_fill, nested_array_func, adjacent_positions

with open("input.txt", "r") as f:
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


# What if we count *CORNERS* insteadof sides?
def num_sides(locations: set[tuple[int, int]]) -> int:
    corners = 0
    for loc in locations:
        n = (loc[0] - 1, loc[1]) in locations
        e = (loc[0], loc[1] + 1) in locations
        s = (loc[0] + 1, loc[1]) in locations
        w = (loc[0], loc[1] - 1) in locations
        ne = (loc[0] - 1, loc[1] + 1) in locations
        se = (loc[0] + 1, loc[1] + 1) in locations
        sw = (loc[0] + 1, loc[1] - 1) in locations
        nw = (loc[0] - 1, loc[1] - 1) in locations

        if w and n and not nw:
            corners += 1
        if n and e and not ne:
            corners += 1
        if e and s and not se:
            corners += 1
        if s and w and not sw:
            corners += 1
        if not n and not w:
            corners += 1
        if not n and not e:
            corners += 1
        if not e and not s:
            corners += 1
        if not s and not w:
            corners += 1
    return corners


print("Regions:")
total_price = 0
for region in regions:
    random_pos = next(iter(region))
    sides = num_sides(region)
    area = len(region)
    price = sides * area
    print(f"region {garden(random_pos)} around "
          f"{random_pos}: "
          f"A={area} S={sides} "
          f"fence price: {price}")
    total_price += price

print(f"{total_price=}")
