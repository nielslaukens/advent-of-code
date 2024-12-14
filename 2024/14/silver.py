import dataclasses
import re

import numpy as np

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
    m = np.zeros(SIZE)
    for robot in robots:
        m[robot.position] += 1
    return m

print(grid(robots).transpose())
for i in range(100):
    for robot in robots:
        robot.step()
m = grid(robots)
print(m.transpose())

quadrant_lt = m[0:(SIZE[0]//2), 0:(SIZE[1]//2)]
quadrant_rt = m[(SIZE[0]//2+1):, 0:(SIZE[1]//2)]
quadrant_lb = m[0:(SIZE[0]//2), (SIZE[1]//2+1):]
quadrant_rb = m[(SIZE[0]//2+1):, (SIZE[1]//2+1):]
quadrant_lt_robots = np.sum(quadrant_lt)
quadrant_rt_robots = np.sum(quadrant_rt)
quadrant_lb_robots = np.sum(quadrant_lb)
quadrant_rb_robots = np.sum(quadrant_rb)

print(quadrant_lt_robots * quadrant_rt_robots * quadrant_lb_robots * quadrant_rb_robots)
