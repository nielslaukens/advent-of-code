from __future__ import annotations
import dataclasses
import re
import typing
import time
from pprint import pprint

import numpy
import tools.tree

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
        machines.append(Machine(numpy.array(switches).transpose(), joltage))


class ButtonPresses:
    def __init__(self, options: numpy.ndarray, num_pushes: numpy.ndarray = None):
        if num_pushes is None:
            num_pushes = numpy.zeros((options.shape[1],), dtype=int)
        self.num_pushes = num_pushes
        self.options = options

    def value(self) -> numpy.ndarray:
        return numpy.matmul(self.options, self.num_pushes)

    def branches(self) -> typing.Generator[ButtonPresses, None, None]:
        for i in range(self.num_pushes.shape[0]):
            # Since the order of the button presses doesn't matter,
            # only generate extra pushes for buttons up to the highest used button
            j = numpy.zeros(self.num_pushes.shape, dtype=int)
            j[i] = 1
            new_num_pushes = self.num_pushes + j
            yield ButtonPresses(self.options, new_num_pushes)
            if self.num_pushes[i] > 0:
                break

    def __str__(self) -> str:
        return f"{self.value()} after {self.num_pushes}"


total_presses = 0
for machine in machines:
    pprint(machine)

    tree = tools.tree.TraverseTreeBreathFirst(
        ButtonPresses(machine.switches),
        lambda n: n.branches(),
    )
    for node in tree:
        v = node.value()
        if numpy.all(v == machine.joltage):
            print(f"[{tree.nodes_visited}] Reached state {v} after pressing {sum(node.num_pushes)} buttons: {node.num_pushes}")
            total_presses += sum(node.num_pushes)
            break
        elif numpy.any(v > machine.joltage):
            tree.dont_descend_into_current_node()


print(total_presses)
print(f"Runtime: {time.time()-start_time:.3f} seconds")
