import dataclasses
import re
import typing


@dataclasses.dataclass
class Instruction:
    state: bool
    x: typing.Tuple[int, int]
    y: typing.Tuple[int, int]
    z: typing.Tuple[int, int]


instructions = []
with open("22.input.txt", "r") as f:
    for line in f.readlines():
        line = line.strip()
        m = re.match(r'(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)', line)
        if not m:
            raise ValueError()
        instructions.append(Instruction(
            state=m.group(1) == 'on',
            x=(int(m.group(2)), int(m.group(3))),
            y=(int(m.group(4)), int(m.group(5))),
            z=(int(m.group(6)), int(m.group(7))),
        ))


def ranges_from_points(
        on_l: int,
        on_h: int,
        carve_l: int,
        carve_h: int
) -> typing.Tuple[typing.List[typing.Tuple[int, int]], typing.Optional[int]]:
    # Ranges are INCLUSIVE: (0, 2) contains 0, 1 and 2
    assert on_l <= on_h
    assert carve_l <= carve_h
    if carve_l <= carve_h < on_l <= on_h:
        # cccc
        #      oooo
        #      0000
        return [(on_l, on_h)], None
    if carve_l <= on_l <= carve_h < on_h:
        # ccccc
        #    oooo
        #    0011
        return [(on_l, carve_h), (carve_h+1, on_h)], 0
    if carve_l <= on_l <= on_h <= carve_h:
        # ccccccccc
        #    oooo
        #    0000
        return [(on_l, on_h)], 0
    if on_l < carve_l <= carve_h < on_h:
        #  cc
        # oooo
        # 0112
        return [(on_l, carve_l-1), (carve_l, carve_h), (carve_h+1, on_h)], 1
    if on_l < carve_l <= on_h <= carve_h:
        #  cccc
        # oooo
        # 0111
        return [(on_l, carve_l-1), (carve_l, on_h)], 1
    if on_l <= on_h < carve_l <= carve_h:
        #    cccc
        # ooo
        # 000
        return [(on_l, on_h)], None


assert ranges_from_points(10, 20, 9, 9) == ([(10, 20)], None)
assert ranges_from_points(10, 20, 9, 10) == ([(10, 10), (11, 20)], 0)
assert ranges_from_points(10, 20, 9, 11) == ([(10, 11), (12, 20)], 0)
assert ranges_from_points(10, 20, 9, 19) == ([(10, 19), (20, 20)], 0)
assert ranges_from_points(10, 20, 9, 20) == ([(10, 20)], 0)
assert ranges_from_points(10, 20, 9, 21) == ([(10, 20)], 0)

assert ranges_from_points(10, 20, 10, 10) == ([(10, 10), (11, 20)], 0)
assert ranges_from_points(10, 20, 10, 11) == ([(10, 11), (12, 20)], 0)
assert ranges_from_points(10, 20, 10, 19) == ([(10, 19), (20, 20)], 0)
assert ranges_from_points(10, 20, 10, 20) == ([(10, 20)], 0)
assert ranges_from_points(10, 20, 10, 21) == ([(10, 20)], 0)

assert ranges_from_points(10, 20, 11, 11) == ([(10, 10), (11, 11), (12, 20)], 1)
assert ranges_from_points(10, 20, 11, 19) == ([(10, 10), (11, 19), (20, 20)], 1)
assert ranges_from_points(10, 20, 11, 20) == ([(10, 10), (11, 20)], 1)
assert ranges_from_points(10, 20, 11, 21) == ([(10, 10), (11, 20)], 1)

assert ranges_from_points(10, 20, 19, 19) == ([(10, 18), (19, 19), (20, 20)], 1)
assert ranges_from_points(10, 20, 19, 20) == ([(10, 18), (19, 20)], 1)
assert ranges_from_points(10, 20, 19, 21) == ([(10, 18), (19, 20)], 1)

assert ranges_from_points(10, 20, 20, 20) == ([(10, 19), (20, 20)], 1)
assert ranges_from_points(10, 20, 20, 21) == ([(10, 19), (20, 20)], 1)

assert ranges_from_points(10, 20, 21, 21) == ([(10, 20)], None)


class Reactor:
    # Ranges are INCLUSIVE! i.e. 0..2 is 3 elements
    def __init__(self):
        self.on_ranges = []

    def _carve_out(self, carve_range) -> typing.List[int]:
        carved_cuboids = []
        new_ranges = []
        for on_range in self.on_ranges:
            original_on_range = list(on_range)  # copy
            maybe_new_ranges = []
            for dimension in range(3):
                split_ranges, overlap_index = ranges_from_points(
                    on_range[dimension][0], on_range[dimension][1],
                    carve_range[dimension][0], carve_range[dimension][1],
                )
                for i, split_range in enumerate(split_ranges):
                    if i != overlap_index:
                        r = list(on_range)  # copy
                        r[dimension] = split_range
                        maybe_new_ranges.append(r)
                if overlap_index is None:  # split was unnecessary
                    new_ranges.append(original_on_range)
                    break
                # else: continue to split up overlapping range
                on_range[dimension] = split_ranges[overlap_index]
            else:  # loop terminated normally
                maybe_new_ranges.append(on_range)
                new_ranges.extend(maybe_new_ranges)
                carved_cuboids.append(len(new_ranges) - 1)  # last one added

        self.on_ranges = new_ranges
        return carved_cuboids

    def switch(self, xyz_range, state: bool):
        carved_cuboids = self._carve_out(xyz_range)
        for carved_cuboid in sorted(carved_cuboids, reverse=True):
            # Remove overlaps, remove from back to front, otherwise indices are changed
            self.on_ranges = self.on_ranges[0:carved_cuboid] + self.on_ranges[(carved_cuboid+1):]
        if state:
            self.on_ranges.append(xyz_range)

    def num_on(self):
        on = 0
        for on_range in self.on_ranges:
            on += (on_range[0][1]-on_range[0][0] + 1) * \
                  (on_range[1][1]-on_range[1][0] + 1) * \
                  (on_range[2][1]-on_range[2][0] + 1)
        return on


reactor = Reactor()
for i, instruction in enumerate(instructions):
    reactor.switch([instruction.x, instruction.y, instruction.z], instruction.state)
    print(f"{i}: {len(reactor.on_ranges)} cuboid sections")
    print(f"{i}: {reactor.num_on()} cubes on")
