import dataclasses
import re
import typing

with open("17.input.txt", "r") as f:
    line = f.readline()
    m = re.match(r'target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)', line)
    target = (
        (int(m.group(1)), int(m.group(2))),
        (int(m.group(3)), int(m.group(4))),
    )


@dataclasses.dataclass
class Probe:
    vel: typing.Tuple[int, int]
    pos: typing.Tuple[int, int] = (0, 0)

    def step(self):
        self.pos = self.pos[0] + self.vel[0], self.pos[1] + self.vel[1]
        velx = self.vel[0]
        if velx > 0:
            velx -= 1
        elif velx > 0:
            velx += 1
        elif velx == 0:
            pass
        else:
            raise ValueError()
        vely = self.vel[1] - 1
        self.vel = velx, vely


def try_launch(vel: typing.Tuple[int, int]) -> typing.Tuple[bool, int]:
    probe = Probe(vel=vel)
    max_y = probe.pos[1]
    while True:
        probe.step()
        #print(f"{probe.pos}")

        if probe.pos[1] > max_y:
            max_y = probe.pos[1]

        if target[0][0] <= probe.pos[0] <= target[0][1] \
                and target[1][0] <= probe.pos[1] <= target[1][1]:
            return True, max_y
        if probe.pos[0] > target[0][1]:  # to the right of the target area, abort
            break
        if probe.pos[1] < target[1][0]:  # below the target area, abort
            break
    return False, None


# X and Y are independent
velx_range = [0, target[0][1]+1]  # immediate overshoot
# We can determine a minimum velocity for X to reach the target
# asymptotical X coordinate for init_velx=N is sum_{vel=1}^{N} =>
# sum_{k=1}^{N} k = N*(N+1)/2
while velx_range[0] * (velx_range[0] + 1) / 2 < target[0][0]:
    velx_range[0] += 1
print(f"x velocity acceptable range: {velx_range[0]}..{velx_range[1]}")

vely_range = [target[1][0]-1, None]  # immediate overshoot
# for upward launches, we will reach y=0 again at -initial_vel_y
# The next step will end us at position y=-initial_vel_y
# This puts an upper limit to vel_y
vely_range[1] = -target[1][0]
print(f"y velocity acceptable range: {vely_range[0]}..{vely_range[1]}")


valid_launches = {}
for vely in range(vely_range[0], vely_range[1]+1):
    for velx in range(velx_range[0], velx_range[1]+1):
        vel = (velx, vely)
        reached, max_y = try_launch(vel)
        if reached:
            valid_launches[vel] = max_y

maxy = 0
maxy_vel = None
for launch, launch_maxy in valid_launches.items():
    if launch_maxy > maxy:
        maxy = launch_maxy
        maxy_vel = launch

print(f"{len(valid_launches) }")
