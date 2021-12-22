import dataclasses
import re
import typing

import numpy


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


reactor = numpy.zeros((100+1, 100+1, 100+1), dtype=bool)
r_offset = -50, -50, -50
def cuboid(
        x_span: typing.Tuple[int, int],
        y_span: typing.Tuple[int, int],
        z_span: typing.Tuple[int, int],
) -> numpy.ndarray:
    cuboid = numpy.zeros(reactor.shape, dtype=bool)
    x_span = (
        max(x_span[0], r_offset[0]),
        min(x_span[1], r_offset[0] + reactor.shape[0])
    )
    y_span = (
        max(y_span[0], r_offset[1]),
        min(y_span[1], r_offset[1] + reactor.shape[1])
    )
    z_span = (
        max(z_span[0], r_offset[2]),
        min(z_span[1], r_offset[2] + reactor.shape[2])
    )
    cuboid[
            (x_span[0] - r_offset[0]):(x_span[1] - r_offset[0] + 1),
            (y_span[0] - r_offset[1]):(y_span[1] - r_offset[1] + 1),
            (z_span[0] - r_offset[2]):(z_span[1] - r_offset[2] + 1),
        ] = True
    return cuboid


for instruction in instructions:
    c = cuboid(instruction.x, instruction.y, instruction.z)
    if instruction.state is True:  # switch on
        reactor = numpy.logical_or(reactor, c)
    else:  # switch off
        reactor = numpy.logical_and(reactor, numpy.logical_not(c))
    print(f"Cubes on: {numpy.sum(reactor)}")
