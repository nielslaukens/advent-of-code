import tools.slices

fresh_ingredient_ranges: list[slice] = []
available_ingredients: list[int] = []

state = 'fresh'
with open("input.txt", "r") as f:
    for line in f:
        line = line.rstrip()

        if line == "":
            state = 'available'
            continue
        if state == 'fresh':
            line = line.split('-')
            fresh_ingredient_ranges.append(slice(int(line[0]), int(line[1]) + 1))  # inclusive end, so +1 for Python
        elif state == 'available':
            available_ingredients.append(int(line))
        else:
            raise RuntimeError(f"Unknown state: {state}")

print(fresh_ingredient_ranges)
print(available_ingredients)

i = tools.slices.Slices()
total_with_overlap = 0
for fresh in fresh_ingredient_ranges:
    i.add(fresh)
    total_with_overlap += fresh.stop - fresh.start

total_without_overlap = 0
for fresh in i:
    total_without_overlap += fresh.stop - fresh.start

print(total_with_overlap)
print(total_without_overlap)
