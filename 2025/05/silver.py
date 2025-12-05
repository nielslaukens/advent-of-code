fresh_ingredient_ranges: list[range] = []
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
            fresh_ingredient_ranges.append(range(int(line[0]), int(line[1]) + 1))  # inclusive end, so +1 for Python
        elif state == 'available':
            available_ingredients.append(int(line))
        else:
            raise RuntimeError(f"Unknown state: {state}")

print(fresh_ingredient_ranges)
print(available_ingredients)

total_fresh = 0
for ingredient in available_ingredients:
    for fresh in fresh_ingredient_ranges:
        if ingredient in fresh:
            total_fresh += 1
            break

print(total_fresh)