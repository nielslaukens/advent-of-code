
with open("6_1.input.txt", "r") as f:
    ages = [
        int(age)
        for age in f.readline().split(',')
    ]

print(f"Initial state: {len(ages)} fish: {ages}")
for day in range(1, 80+1):
    new_ages = []
    for i, age in enumerate(ages):
        if age == 0:
            new_ages.append(6)
            new_ages.append(8)
        else:
            new_ages.append(age-1)
    ages = new_ages
    print(f"State after {day} days: {len(ages)} fish")
