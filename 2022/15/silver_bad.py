import dataclasses
import enum
import functools
import re

import numpy as np

from tools import numpy_tools
from tools.infinite_grid import InfiniteGrid

#filename = "sample.txt"
#solution_y = 10
filename = "input.txt"
solution_y = 2000000


def manhattan_distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class State(int, enum.Enum):
    Unknown = 0
    Safe = 1
    Sensor = 2
    Beacon = 3


@dataclasses.dataclass
class SensorData:
    sensor_position: tuple[int, int]
    nearest_beacon: tuple[int, int]

    @functools.cached_property
    def manhattan_distance_to_nearest_beacon(self) -> int:
        return manhattan_distance(self.sensor_position, self.nearest_beacon)

    def at_pos(self, coord: tuple[int, int]) -> State:
        if coord == self.sensor_position:
            return State.Sensor
        if coord == self.nearest_beacon:
            return State.Beacon
        if manhattan_distance(self.sensor_position, coord) <= self.manhattan_distance_to_nearest_beacon:
            return State.Safe
        return State.Unknown


min_x = max_x = min_y = max_y = 0
sensors: list[SensorData] = []
with open(filename, "r") as f:
    for line in f:
        match = re.match(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)',
                         line)
        if not match:
            raise ValueError(line)

        sensor = (int(match.group(1)), int(match.group(2)))
        beacon = (int(match.group(3)), int(match.group(4)))

        min_x = min(min_x, sensor[0], beacon[0])
        min_y = min(min_y, sensor[1], beacon[1])
        max_x = max(max_x, sensor[0], beacon[0])
        max_y = max(max_y, sensor[1], beacon[1])

        sensors.append(SensorData(
            sensor_position=sensor,
            nearest_beacon=beacon,
        ))


num_safe = 0
for x in range(min_x, max_x+1):
    if x % 10000 == 0:
        print(x, num_safe)
    c = (x, solution_y)
    state = State.Unknown
    for sensor in sensors:
        state_according_to_sensor = sensor.at_pos(c)
        if state_according_to_sensor.value > state.value:
            state = state_according_to_sensor
        if state.value > State.Safe.value:
            # Beacon and/or Sensor don't count as Safe.
            # So once there is "something" there, stop checking other sensors.
            break
    if state == State.Safe:
        num_safe += 1

print(num_safe)
# 4432197 too low
