with open('input.txt', 'r') as f:
    lines = [
        line.strip()
        for line in f.readlines()
    ]

position = 50
times_at_0 = 0
for line in lines:
    direction = line[0]
    amount = int(line[1:])
    new_position = (position + (-1 if direction == "L" else 1) * amount) % 100
    print(f"{position} {direction} {amount} => {new_position}")
    position = new_position
    if position == 0:
        times_at_0 += 1

print(times_at_0)
