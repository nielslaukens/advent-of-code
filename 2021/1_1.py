prev_depth = None
num_increases = 0

with open("1_1.input.txt", "r") as f:
    for line in f.readlines():
        depth = int(line)
        if prev_depth is not None:
            if depth > prev_depth:
                num_increases += 1
        prev_depth = depth

print(num_increases)