from __future__ import annotations
import dataclasses
import re
import typing
import time
from pprint import pprint

import numpy
import scipy.optimize

start_time = time.time()


@dataclasses.dataclass
class Machine:
    switches: list[numpy.ndarray]
    joltage: numpy.ndarray


machines = []
with open("input.txt") as f:
    for line in f:
        line = line.rstrip()
        m = re.fullmatch(r'\[([.#]+)] ([^{]+){(.*)}', line)
        switches = m.group(2)[1:-2]  # strip starting '(' and ending ') '
        switches = [
            [int(pos) for pos in switch.split(',')]
            for switch in switches.split(') (')]
        joltage = numpy.array([int(num) for num in m.group(3).split(',')])

        for i, switch in enumerate(switches):
            n = numpy.zeros(joltage.shape, dtype=int)
            for pos in switch:
                n[pos] = 1
            switches[i] = n

        switches = sorted(switches, key=lambda x: sum(x), reverse=True)
        machines.append(Machine(numpy.array(switches).transpose(), joltage))


total_presses = 0
for i, machine in enumerate(machines):
    print(f"{i}/{len(machines)}: ")
    pprint(machine)

    c = numpy.array([1]*machine.switches.shape[1])

    res = scipy.optimize.linprog(
        c,
        A_eq=machine.switches,
        b_eq=machine.joltage,
        integrality=1,
    )
    print(f"{res.x} ({res.fun}) => {numpy.matmul(machine.switches, res.x)}")
    total_presses += round(res.fun)


print(total_presses)
print(f"Runtime: {time.time()-start_time:.3f} seconds")
