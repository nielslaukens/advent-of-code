
age_bags = {
    age: 0
    for age in range(0, 8+1)
}
with open("6_1.input.txt", "r") as f:
    for age in f.readline().split(','):
        age_bags[int(age)] += 1


def total_fish():
    t = 0
    for num_fish in age_bags.values():
        t += num_fish
    return t

print(f"Initial state: {total_fish()}: {list(age_bags.values())}")
for day in range(1, 256+1):
    new_age_bags = {_: 0 for _ in range(0, 8+1)}
    for age, num_fish in age_bags.items():
        if age == 0:
            new_age_bags[6] += num_fish
            new_age_bags[8] += num_fish
        else:
            new_age_bags[age-1] += num_fish
    age_bags = new_age_bags
    print(f"State after {day} days: {total_fish()}: {list(age_bags.values())}")
