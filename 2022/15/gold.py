from __future__ import annotations
import dataclasses
import re

from tools.slices import Slices

# filename = "sample.txt"
# solution_max = 20
filename = "input.txt"
solution_max = 4000000


def manhattan_distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


@dataclasses.dataclass
class Sensor:
    position: tuple[int, int]
    nearest_beacon_position: tuple[int, int]

    @property
    def manhattan_distance_to_beacon(self) -> int:
        return manhattan_distance(self.position, self.nearest_beacon_position)

    def safe(self, y: int) -> slice | None:
        dy = abs(self.position[1] - y)
        dx = self.manhattan_distance_to_beacon - dy
        if dx < 0:
            return None
        else:
            return slice(self.position[0] - dx, self.position[0] + dx + 1)


sensors: list[Sensor] = []
with open(filename, "r") as f:
    for line in f:
        match = re.match(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)',
                         line)
        if not match:
            raise ValueError(line)

        sensor = (int(match.group(1)), int(match.group(2)))
        beacon = (int(match.group(3)), int(match.group(4)))

        sensors.append(Sensor(
            position=sensor,
            nearest_beacon_position=beacon,
        ))

for y in range(0, solution_max):
    possible_beacon_pos = Slices([slice(0, solution_max + 1)])
    for sensor in sensors:
        safe_for_this_sensor = sensor.safe(y=y)
        if safe_for_this_sensor is not None:
            possible_beacon_pos.remove(safe_for_this_sensor)

    if len(possible_beacon_pos):
        assert len(possible_beacon_pos) == 1
        assert possible_beacon_pos._ranges[0].stop == possible_beacon_pos._ranges[0].start + 1
        x = possible_beacon_pos._ranges[0].start
        print(f"Possible beacon location at x={x} y={y} => {x*4000000 + y}")
