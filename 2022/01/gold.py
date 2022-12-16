elve_calories = [[]]

with open("input.txt", "r") as f:
    for line in f:
        line = line.rstrip()
        if line != "":
            elve_calories[-1].append(int(line))
        else:
            elve_calories.append([])

for i, elve in enumerate(elve_calories):
    sum = 0
    for food in elve:
        sum += food
    elve_calories[i] = sum

a = sorted(elve_calories, reverse=True)
print(a[0] + a[1] + a[2])
