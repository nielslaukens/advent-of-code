import enum
import functools


class Color(enum.Enum):
    White = 'w'
    Blue = 'u'
    Black = 'b'
    Red = 'r'
    Green = 'g'


designs = []
with open("input.txt", "r") as f:
    towels = [
        towel.strip()
        for towel in f.readline().strip().split(',')
    ]
    empty_line = f.readline()
    assert empty_line == "\n"
    for design in f:
        design = design.strip()
        designs.append(design)

print(towels)
print(designs)


def pretty_print(s: list[str]) -> str:
    seq = ''
    color = 0
    for towel in s:
        if color:
            seq += "\033[91m" + towel + "\033[0m"
        else:
            seq += "\033[92m" + towel + "\033[0m"
        color = 1 - color
    return seq


@functools.lru_cache(maxsize=1024*1024)
def search_remaining(design: str) -> int:
    matches = 0
    for towel in towels:
        if towel == design:
            # full match
            matches += 1
        elif towel == design[0:len(towel)]:
            # partial match, try to match the rest
            rest = design[len(towel):]
            rest_matches = search_remaining(rest)
            matches += rest_matches
    return matches


designs_possible = 0
total_possibilities = 0
for design in designs:
    search_remaining.cache_clear()
    possibilities = search_remaining(design)
    print(f"{design}: {possibilities}")
    designs_possible += 1 if possibilities else 0
    total_possibilities += possibilities

print(f"{designs_possible} designs possible, {total_possibilities} total possibilities")
