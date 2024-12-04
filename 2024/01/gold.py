import itertools

left_list = []
right_list = []

with open("input.txt", "r") as f:
    for line in f.readlines():
        left, right = line.split()
        left_list.append(int(left))
        right_list.append(int(right))

right_count = {}
for right in right_list:
    right_count[right] = right_count.get(right, 0) + 1

similarity_score = 0
for left in left_list:
    similarity_score += left * right_count.get(left, 0)

print(similarity_score)
