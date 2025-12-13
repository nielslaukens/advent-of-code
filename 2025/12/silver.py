from __future__ import annotations
import dataclasses
import time
import re
import typing

import numpy

import tools.tree

start_time = time.time()

@dataclasses.dataclass
class Region:
    width: int
    length: int
    quantity: list[int]

shapes: list[numpy.ndarray] = []
regions = []

with open("input.txt", "r") as file:
    state = "shape number"
    shape = []

    for line in file:
        line = line.rstrip()
        if state == "shape number":
            m = re.fullmatch(r'(\d+):', line)
            if m:
                shape_num = int(m.group(1))
                state = "shape"
                continue
            else:
                state = "regions"
                # fall through immediately

        if state == "shape":
            if line != "":
                shape.append([1 if char == "#" else 0 for char in line])
            else:
                assert shape_num == len(shapes)
                shapes.append(numpy.array(shape))
                shape = []
                state = "shape number"

        if state == "regions":
            m = re.fullmatch(r'(\d+)x(\d+): ([0123456789 ]+)', line)
            if not m:
                raise ValueError(f"Bad line {state}: {line}")
            region = Region(
                width=int(m.group(1)),
                length=int(m.group(2)),
                quantity=[int(_) for _ in m.group(3).split(' ')]
            )
            regions.append(region)

#print(shapes)
#print(regions)

def orientations(shape: numpy.ndarray) -> list[numpy.ndarray]:
    def rotations(shape: numpy.ndarray) -> list[numpy.ndarray]:
        o = [shape]
        t = numpy.transpose(shape)
        l90 = numpy.flip(t, axis=1)  # left 90º
        o.append(l90)
        r90 = numpy.flip(numpy.flip(l90, axis=0), axis=1)  # right 90º
        o.append(r90)
        half = numpy.flip(numpy.flip(shape, axis=0), axis=1)  # 180º
        o.append(half)
        return o
    all = [
        *rotations(shape),
        *rotations(numpy.flip(shape, axis=0)),
    ]
    dedup = []
    for shape in all:
        different = True
        for candidate in dedup:
            if numpy.all(candidate == shape):
                different = False
                break
        if different:
            dedup.append(shape)
    return dedup

# pre-rotate the shapes
num_spots = []
for i, shape in enumerate(shapes):
    num_spots.append(numpy.sum(shape))
    shapes[i] = orientations(shape)
    #print(f"{i}: {len(shapes[i])}")


def place(present: numpy.ndarray, region: numpy.ndarray, position: tuple[int, int]) -> numpy.ndarray:
    pad = [
        (position[0], region.shape[0]-3-position[0]),
        (position[1], region.shape[1]-3-position[1]),
    ]
    padded_present = numpy.pad(present, pad, mode="constant", constant_values=0)
    return region + padded_present


class Node:
    def __init__(
            self,
            region: numpy.ndarray,
            presents_to_place: list[int],
            position: tuple[int, int] |  None = None,
    ):
        self.region = region
        self.presents_to_place = presents_to_place
        self._position = position

    def __str__(self):
        return str(self.region)

    def branches(self) -> typing.Generator[Node, None, None]:
        if self._position is None:
            if len(self.presents_to_place) == 0:
                return

            for y in range(0, self.region.shape[0] - 3 + 1):
                for x in range(0, self.region.shape[1] - 3 + 1):
                    yield Node(
                        self.region,
                        self.presents_to_place,
                        (y, x),
                    )
        else:
            for o in shapes[self.presents_to_place[0]]:
                r = place(o, self.region, self._position)
                yield Node(r, self.presents_to_place[1:], None)

regions_with_solutions = 0
for reg_num, region in enumerate(regions):
    r = numpy.zeros((region.length, region.width))
    presents_to_place = []
    locations_to_use = 0
    blocks_to_place = 0
    for p, q in enumerate(region.quantity):
        for i in range(q):
            presents_to_place.append(p)
            locations_to_use += num_spots[p]
            blocks_to_place += 1

    if locations_to_use > region.length * region.width:
        print(f"{reg_num}/{len(regions)} Will never fit")
        continue
    if blocks_to_place <= (region.length//3) * (region.width//3):
        print(f"{reg_num}/{len(regions)} Will definitely fit")
        regions_with_solutions += 1
        continue

    # turns out, we never need this:
    tree = tools.tree.TraverseTreeDepthFirstPre(
        Node(r, presents_to_place),
        lambda n: n.branches(),
    )
    for node in tree:
        if node._position is None and numpy.any(node.region > 1):
            # we already have an overlap
            tree.dont_descend_into_current_node()
            continue
        if len(node.presents_to_place) == 0:
            print(f"{reg_num}/{len(regions)}: Found a solution")
            #print(node.region)
            regions_with_solutions += 1
            break

print(regions_with_solutions)
print(f"took {time.time() - start_time:.3f} seconds")
