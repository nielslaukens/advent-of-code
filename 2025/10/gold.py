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
        machines.append(Machine(switches, joltage))


class Node:
    def __init__(self, options: numpy.ndarray, pushes: numpy.ndarray = None):
        if pushes is None:
            pushes = numpy.zeros((options.shape[1],), dtype=int)
        self.options = options
        self.pushes = pushes
        self._value = None

    def branches(self) -> typing.Generator[Node, None, None]:
        for i in range(self.options.shape[1]):
            if i < self.options.shape[1]-1 and self.pushes[i+1] != 0:
                continue
            j = numpy.zeros(self.pushes.shape, dtype=int)
            j[i] = 1
            pushes = self.pushes + j
            yield Node(self.options, pushes)

    def __str__(self) -> str:
        return f"{self.pushes} => {self.value()}"

    def value(self) -> numpy.ndarray:
        if self._value is None:
            self._value = numpy.matmul(self.options, self.pushes)
        return self._value


total_presses = 0
for machine in machines:
    pprint(machine)
    tree = tools.tree.TraverseTreeDepthFirstPre(
        Node(numpy.array(sorted(machine.switches, key=lambda e: sum(e), reverse=True)).transpose()),
        lambda n: n.branches(),
    )
    for node in tree:
        if tree.nodes_visited % 1_000_000 == 0:
            print(tree.nodes_visited, node)
        v = node.value()
        if numpy.all(v == machine.joltage):
            print(f"Found {node.value()} after {tree.nodes_visited} with {sum(node.pushes)} pushes")
            total_presses += sum(node.pushes)
            break
        if numpy.any(v > machine.joltage):
            tree.dont_descend_into_current_node()

print(total_presses)
print(f"Runtime: {time.time()-start_time:.3f} seconds")
