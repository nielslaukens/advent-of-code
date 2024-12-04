import itertools

left_list = []
right_list = []

with open("input.txt", "r") as f:
    for line in f.readlines():
        left, right = line.split()
        left_list.append(int(left))
        right_list.append(int(right))

left_list = sorted(left_list)
right_list = sorted(right_list)
total_dist = 0
for l, r in itertools.zip_longest(left_list, right_list):
    diff = abs(l - r)
    print(l, r, diff)
    total_dist += diff

print(total_dist)
