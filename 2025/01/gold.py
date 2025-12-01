with open('input.txt', 'r') as f:
    lines = [
        line.strip()
        for line in f.readlines()
    ]

position = 50
MOD = 100

times_at_0 = 0
for line in lines:
    direction = line[0]
    amount = int(line[1:])
    delta = (-1 if direction == "L" else 1) * amount

    new_position = position + delta
    # case: 95 R5 L5
    t0 = 0
    if (position == 0 and new_position < 0) \
            or (position == MOD and new_position > MOD):
        # already counted after previous move
        t0 -= 1
    while new_position < 0:
        new_position += MOD
        t0 += 1
    while new_position > MOD:
        new_position -= MOD
        t0 += 1
    if new_position == 0 or new_position == MOD:
        t0 += 1

    print(f"{position:02d} {direction}{amount:02d} => {new_position:02d}  {t0}")
    position = new_position
    times_at_0 += t0

print(times_at_0)
