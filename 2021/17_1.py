import dataclasses
import re
import typing

with open("17.input.txt", "r") as f:
    # target area: x=211..232, y=-124..-69
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
# We can dete
# rmine a minimum velocity for X to reach the target
# asymptotical X coordinate for init_velx=N is sum_{vel=1}^{N} =>
# sum_{k=1}^{N} k = N*(N+1)/2
velx_min = 0
while velx_min * (velx_min + 1) / 2 < target[0][0]:
    velx_min += 1

velx_max = target[0][1]  # immediate overshoot
print(f"x velocity acceptable range: {velx_min}..{velx_max}")


valid_launches = {}
for vely in range(0, 200):
    for velx in range(velx_min, velx_max):
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

print(f"Launch at {maxy_vel} reaches {maxy}")
