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

        switches = sorted(switches, key=lambda x: sum(x), reverse=True)
        machines.append(Machine(numpy.array(switches), joltage))


def splits(total: int, parts: int) -> typing.Generator[tuple[int, ...], None, None]:
    if parts == 0:
        return
    if parts == 1:
        yield (total,)
        return
    for i in range(total, -1, -1):
        for rest in splits(total - i, parts - 1):
            yield i, *rest

assert list(splits(5, 0)) == []
assert list(splits(5, 1)) == [(5,)]
assert list(splits(5, 2)) == [(5,0), (4,1), (3,2), (2,3), (1,4), (0,5)]
assert list(splits(2, 3)) == [(2,0,0), (1,1,0), (1,0,1), (0,2,0), (0,1,1), (0,0,2)]


def do_digit(digit_num: int, switches: list[numpy.ndarray], total: int) -> typing.Generator[tuple[int, ...], None, None]:
    switches_for_this_digit = []
    for i, switch in enumerate(switches):
        if switch[digit_num]:
            switches_for_this_digit.append(i)
    for split in splits(total, len(switches_for_this_digit)):
        num_pushes = [0] * len(switches)
        for i, j in enumerate(switches_for_this_digit):
            num_pushes[j] = split[i]
        yield tuple(num_pushes)


class Node:
    def __init__(
            self,
            joltage: numpy.ndarray,
            switches: numpy.ndarray,
            pushes: numpy.ndarray = None,
            digits_to_do: list[int] = None
    ):
        if pushes is None:
            pushes = numpy.zeros((len(switches),), dtype=int)
        if digits_to_do is None:
            digits_to_do = list(range(len(joltage)))

        self.joltage = joltage
        self.switches = switches
        self.pushes = pushes
        self._value = None

        # Do digits in the best order:
        switches_affecting_digit = switches.sum(axis=0)
        remaining_joltage = joltage - self.value()
        digits_to_do = sorted(digits_to_do, key=lambda d: remaining_joltage[d] ** switches_affecting_digit[d])
        self.digits_to_do = digits_to_do

    def __str__(self) -> str:
        return f"digits to do: {self.digits_to_do}; pushes {self.pushes} => {self.joltage - self.value()}"

    def value(self) -> numpy.ndarray:
        if self._value is None:
            self._value = numpy.matmul(self.pushes, self.switches)
        return self._value

    def branches(self):
        if len(self.digits_to_do) == 0:
            return

        digit_to_do = self.digits_to_do[0]
        v = self.value()
        remaining = self.joltage[digit_to_do] - v[digit_to_do]
        for pushes in do_digit(digit_to_do, self.switches, remaining):
            yield Node(
                self.joltage,
                self.switches,
                self.pushes + pushes,
                self.digits_to_do[1:],
            )


total_presses = 0
for i, machine in enumerate(machines):
    print(f"{i}/{len(machines)}: ")
    pprint(machine)

    tree = tools.tree.TraverseTreeDepthFirstPre(
        Node(
            machine.joltage,
            machine.switches,
        ),
        lambda n: n.branches(),
    )
    least = None
    for node in tree:
        # if tree.nodes_visited % 1_000_000 == 0:
        #     print(node)
        v = node.value()
        if numpy.any(v > machine.joltage):
            tree.dont_descend_into_current_node()
            continue
        #print(node)
        if numpy.all(v == machine.joltage):
            p = sum(node.pushes)
            print(f"Found {p} {node.pushes} after {tree.nodes_visited} tries")
            if least is None or p < least:
                least = p
                break  # TODO: is this valid?

    total_presses += least

print(total_presses)
print(f"Runtime: {time.time()-start_time:.3f} seconds")
