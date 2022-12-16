from __future__ import annotations


class Range:
    def __init__(self, r: str):
        start, stop_incl = r.split('-')
        self.start = int(start)
        self.stop_incl = int(stop_incl)

    def __str__(self) -> str:
        return f"{self.start}-{self.stop_incl}"

    def fully_contains(self, r2: Range) -> bool:
        return self.start <= r2.start and r2.stop_incl <= self.stop_incl

    def partially_overlaps(self, r2: Range) -> bool:
        return r2.start <= self.start <= r2.stop_incl or \
            r2.start <= self.stop_incl <= r2.stop_incl


fully_contained_pairs = 0
partial_overlap_pairs = 0

with open("input.txt", "r") as f:
    for line in f:
        line = line.rstrip()
        elf1, elf2 = line.split(',')
        elf1 = Range(elf1)
        elf2 = Range(elf2)
        if elf1.fully_contains(elf2) or elf2.fully_contains(elf1):
            fully_contained_pairs += 1
        if elf1.partially_overlaps(elf2) or elf2.partially_overlaps(elf1):
            partial_overlap_pairs += 1

print(f"part 1: {fully_contained_pairs}")
print(f"part 2: {partial_overlap_pairs}")
