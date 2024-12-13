import dataclasses

import numpy as np


@dataclasses.dataclass
class Machine:
    button_a: tuple[int, int]
    button_b: tuple[int, int]
    prize: tuple[int, int]


machines: list[Machine] = []
with open("input.txt", "r") as f:
    m = Machine(None, None, None)
    for line in f.readlines():
        line = line.strip()
        if line == "":
            machines.append(m)
            m = Machine(None, None, None)
        elif line.startswith("Button "):
            button = line[len("Button "):]
            button = button[:1]
            coord = line[len("Button A: "):]
            coord = coord.split(", ")
            assert coord[0].startswith('X+')
            assert coord[1].startswith('Y+')
            coord = (int(coord[0][2:]), int(coord[1][2:]))
            if button == "A":
                m.button_a = coord
            elif button == "B":
                m.button_b = coord
        elif line.startswith("Prize: "):
            coord = line[len("Prize: "):]
            coord = coord.split(", ")
            assert coord[0].startswith('X=')
            assert coord[1].startswith('Y=')
            coord = (int(coord[0][2:]), int(coord[1][2:]))
            coord = (coord[0] + 10000000000000, coord[1] + 10000000000000)
            m.prize = coord
        else:
            print("Unknown line", line)
    machines.append(m)

total_cost = 0
for machine in machines:
    # we need to find k, l such that
    # k * buttonA + l * buttonB = prize
    print(machine)
    base = np.array([[machine.button_a[0], machine.button_a[1]],
                     [machine.button_b[0], machine.button_b[1]]]).transpose()
    invbase = np.linalg.inv(base)
    prize = np.array([[machine.prize[0]], [machine.prize[1]]])
    new_coords = np.matmul(invbase, prize)
    # new_coords is in floating point, check if we actually found something:
    new_coords = (new_coords[0][0], new_coords[1][0])
    new_coords_int = (round(new_coords[0]), round(new_coords[1]))
    if new_coords_int[0] * machine.button_a[0] + new_coords_int[1] * machine.button_b[0] == machine.prize[0] and \
            new_coords_int[0] * machine.button_a[1] + new_coords_int[1] * machine.button_b[1] == machine.prize[1]:
        # confirmed
        cost = 3*new_coords_int[0] + 1*new_coords_int[1]
        print(f"{new_coords_int} => {cost}")
        total_cost += cost
    else:
        print("not", new_coords)

print(total_cost)
