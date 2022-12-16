from __future__ import annotations
import dataclasses
import re

from tools.slices import Slices

# filename = "sample.txt"
# solution_y = 10
filename = "input.txt"
solution_y = 2000000


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

safe_range = Slices()
for sensor in sensors:
    safe_for_this_sensor = sensor.safe(y=solution_y)
    if safe_for_this_sensor is not None:
        safe_range.add(safe_for_this_sensor)
    if sensor.position[1] == solution_y:
        safe_range.remove(slice(sensor.position[0], sensor.position[0] + 1))
    if sensor.nearest_beacon_position[1] == solution_y:
        safe_range.remove(slice(sensor.nearest_beacon_position[0], sensor.nearest_beacon_position[0] + 1))

print(safe_range)
print(len(safe_range))
