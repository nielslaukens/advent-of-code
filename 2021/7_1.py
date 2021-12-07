import math

with open("7_1.input.txt", "r") as f:
    crab_initial_positions = [
        int(_)
        for _ in f.readline().strip().split(',')
    ]

crab_initial_position_buckets = {}
min_pos, max_pos = math.inf, -math.inf
for pos in crab_initial_positions:
    crab_initial_position_buckets[pos] = crab_initial_position_buckets.get(pos, 0) + 1
    if pos < min_pos:
        min_pos = pos
    if pos > max_pos:
        max_pos = pos

# Naive approach: try all final positions:
fuel_req = {}
for final_position in range(min_pos, max_pos+1):
    fuel_req[final_position] = 0
    for pos, num_crabs in crab_initial_position_buckets.items():
        fuel_req[final_position] += num_crabs * abs(pos - final_position)

min_fuel_pos = sorted(fuel_req, key=fuel_req.get)[0]
print(f"Minimal fuel ({fuel_req[min_fuel_pos]}) at position {min_fuel_pos}")
