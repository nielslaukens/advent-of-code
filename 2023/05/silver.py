import dataclasses
import math


class Mapping:
    @dataclasses.dataclass
    class Map:
        source_start: int
        dest_start: int
        length: int

    def __init__(self, source: str, dest: str):
        self.source = source
        self.dest = dest
        self.ranges: list[Mapping.Map] = []

    def add_range(self, dest_start: int, source_start: int, length: int):
        self.ranges.append(Mapping.Map(source_start=source_start, dest_start=dest_start, length=length))
        # self.ranges = sorted(self.ranges, key=lambda m: m.source_start)

    def __repr__(self) -> str:
        return f"<Mapping {self.source} -> {self.dest}: {self.ranges}>"

    def __getitem__(self, item: int) -> int:
        for range in self.ranges:
            if range.source_start <= item < range.source_start + range.length:
                return range.dest_start + (item - range.source_start)
        return item


mappings = {}
with open("input.txt", "r") as f:
    line_iter = iter(f)
    seeds = next(line_iter).rstrip()
    assert seeds.startswith("seeds: ")
    seeds = [int(_) for _ in seeds[7:].split()]

    assert next(line_iter).rstrip() == ""

    while True:  # until StopIteration
        try:
            map_name = next(line_iter).rstrip()
        except StopIteration:
            break

        assert map_name.endswith(" map:")
        source, dest = map_name[:-5].split('-to-')
        mapping = Mapping(source=source, dest=dest)

        while True:
            try:
                map_line = next(line_iter).rstrip()
            except StopIteration:
                break
            if map_line == "":
                break

            dest_start, source_start, length = [int(_) for _ in map_line.split()]
            mapping.add_range(dest_start=dest_start, source_start=source_start, length=length)

        mappings[mapping.source] = mapping

min_location = math.inf
for seed_num in seeds:
    resource = 'seed'
    resource_num = seed_num
    #print(f"{resource} {resource_num}")
    while resource != 'location':
        new_resource_num = mappings[resource][resource_num]
        new_resource = mappings[resource].dest
        resource_num = new_resource_num
        resource = new_resource
        #print(f"{resource} {resource_num}")

    print(f"seed {seed_num} => location {resource_num}")
    if resource_num < min_location:
        min_location = resource_num

print(f"Min location: {min_location}")
