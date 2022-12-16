s = 0


def prio_from_item(item: str) -> int:
    if ord(item) >= ord('a'):
        return 1 + ord(item) - ord('a')
    else:  # uppercase
        return 27 + ord(item) - ord('A')


with open("input.txt") as f:
    for line in f:
        line = line.rstrip()
        comp1 = line[0:(len(line)//2)]
        comp2 = line[(len(line)//2):]

        comp1 = set(comp1)
        comp2 = set(comp2)
        both = comp1.intersection(comp2)
        assert len(both) == 1
        both = list(both)[0]

        s += prio_from_item(both)

print(s)
