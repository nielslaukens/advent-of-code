group = []


def prio_from_item(item: str) -> int:
    if ord(item) >= ord('a'):
        return 1 + ord(item) - ord('a')
    else:  # uppercase
        return 27 + ord(item) - ord('A')


with open("input.txt") as f:
    for i, line in enumerate(f):
        line = line.rstrip()
        rucksack = set(line)

        if i % 3 == 0:
            group.append([rucksack])
        else:
            group[-1].append(rucksack)

s = 0
for g in group:
    badge = g[0].intersection(g[1]).intersection(g[2])
    assert len(badge) == 1
    badge = list(badge)[0]
    prio = prio_from_item(badge)
    s += prio

print(s)
