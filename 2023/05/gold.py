import math

import tools.mapping


class Mapping(tools.mapping.Mapping):
    def __init__(self, source: str, dest: str):
        super().__init__()
        self.source = source
        self.dest = dest


mappings = {}
with open("input.txt", "r") as f:
    line_iter = iter(f)
    seeds = next(line_iter).rstrip()
    assert seeds.startswith("seeds: ")
    seeds = [int(_) for _ in seeds[7:].split()]
    seeds = [slice(start, start+length) for start, length in  zip(seeds[::2], seeds[1::2])]

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


def min_location(slices: list[slice]) -> int:
    min_location = math.inf
    for sl in slices:
        if sl.start < min_location:
            min_location = sl.start
    return min_location


class RangeWithHistory:
    def __init__(self, start, stop, history=None) -> None:
        self.start = start
        self.stop = stop

        if history is None:
            history = []
        self.history = history

    def __repr__(self) -> str:
        return f"{self.start}:{self.stop}"


resource = 'seed'
resource_slices = [RangeWithHistory(_.start, _.stop) for _ in seeds]
#print(f"{resource} {resource_num}")
while resource != 'location':
    new_resource = mappings[resource].dest
    print(f"mapping {resource} to {new_resource}")
    new_resource_slices = []
    for sl in resource_slices:
        new_sl = mappings[resource].map_slices([sl])
        new_sl = [
            RangeWithHistory(_.start, _.stop, [*sl.history, f"{resource} {sl}"])
            for _ in new_sl
        ]
        new_resource_slices.extend(new_sl)

    resource_slices = new_resource_slices
    resource = new_resource
    #print(f"{resource} {resource_num}")

print(resource_slices)
print(min_location(resource_slices))
