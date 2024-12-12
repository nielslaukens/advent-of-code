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


def perimeter(locations: set[tuple[int, int]]) -> int:
    """
    Calculate the perimeter of a set of locations.
    Each block has a perimeter of 4, but adjacent blocks reduce this number.
    2D only
    """
    perimeter = 0
    already_counted: set[tuple[int, int]] = set()
    for location in locations:
        perimeter += 4
        for adj in adjacent_positions(location):
            if adj in already_counted:
                perimeter -= 2
        already_counted.add(location)
    return perimeter


print("Regions:")
total_price = 0
for region in regions:
    random_pos = next(iter(region))
    perim = perimeter(region)
    area = len(region)
    price = perim * area
    print(f"region {garden(random_pos)} around "
          f"{random_pos}: "
          f"A={area} P={perim} "
          f"fence price: {price}")
    total_price += price

print(f"{total_price=}")
