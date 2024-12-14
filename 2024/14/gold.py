import dataclasses
import re

import numpy as np
from PIL import Image

SIZE = (101, 103)
#SIZE = (11, 7)


@dataclasses.dataclass
class Robot:
    position: tuple[int, int]
    velocity: tuple[int, int]

    def step(self):
        x, y = (
            self.position[0] + self.velocity[0],
            self.position[1] + self.velocity[1],
        )
        while x < 0:
            x += SIZE[0]
        while SIZE[0] <= x:
            x -= SIZE[0]
        while y < 0:
            y += SIZE[1]
        while SIZE[1] <= y:
            y -= SIZE[1]
        self.position = x, y


robots: list[Robot] = []
with open("input.txt", "r") as f:
    for line in f.readlines():
        match = re.match(r'p=(?P<x>\d+),(?P<y>\d+) v=(?P<vx>-?\d+),(?P<vy>-?\d+)', line)
        m = match.groupdict()
        robot =Robot((int(m['x']), int(m['y'])), (int(m['vx']), int(m['vy'])))
        robots.append(robot)
        #print(robot)


def grid(robots):
    m = np.zeros(SIZE, dtype=np.uint8)
    for robot in robots:
        m[robot.position] += 1
    return m


def save_grid(grid: np.ndarray, i: int):
    im = Image.fromarray(grid * 128)
    im.save(f"/tmp/{i:04d}.bmp")


#save_grid(grid(robots), 0)

for i in range(8179):
    print(f"iter {i}")
    for robot in robots:
        robot.step()
        #m = grid(robots)
        #save_grid(m, i+1)
m = grid(robots)
save_grid(m, 8179)
# 8179 by visual inspection
