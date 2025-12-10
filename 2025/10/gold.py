from __future__ import annotations
import dataclasses
import re
import typing
import time
from pprint import pprint

import tools.tree

start_time = time.time()


class Joltage:
    def __init__(self, jolts: list[int]):
        self.jolts = list(jolts)

    @classmethod
    def zero(cls, length: int) -> Joltage:
        return cls([0] * length)

    def __str__(self) -> str:
        return str(self.jolts)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self.jolts)})"

    def __eq__(self, other: typing.Any) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.jolts == other.jolts

    def bump(self, which_ones: list[int]) -> Joltage:
        o = Joltage(self.jolts)
        for j in which_ones:
            o.jolts[j] += 1
        return o


j = Joltage.zero(4)
j = j.bump([0, 1, 3])
assert j.jolts == [1, 1, 0, 1]
j = j.bump([1, 2])
assert j.jolts == [1, 2, 1, 1]


@dataclasses.dataclass
class Machine:
    switches: list[list[int]]
    joltage: Joltage


machines = []
with open("input.txt") as f:
    for line in f:
        line = line.rstrip()
        m = re.fullmatch(r'\[([.#]+)] ([^{]+){(.*)}', line)
        switches = m.group(2)[1:-2]  # strip starting '(' and ending ') '
        switches = [[int(pos) for pos in switch.split(',')] for switch in switches.split(') (')]
        joltage = Joltage([int(num) for num in m.group(3).split(',')])
        machines.append(Machine(switches, joltage))


class ButtonPresses:
    def __init__(self, joltage: Joltage, options: list[list[int]], history: list[int] = None):
        if history is None:
            history = [0] * len(options)
        self.state = joltage
        self.options = options
        self.history = history

    def branches(self) -> typing.Generator[ButtonPresses, None, None]:
        for i, t in enumerate(self.options):
            # Since the order of the button presses doesn't matter,
            h = list(self.history)
            h[i] += 1
            l = self.state.bump(t)
            yield ButtonPresses(l, self.options, h)
            if self.history[i] > 0:
                break

    def __str__(self) -> str:
        return f"{self.state} after {self.history}"


total_presses = 0
for machine in machines:
    pprint(machine)

    tree = tools.tree.TraverseTreeBreathFirst(
        ButtonPresses(Joltage.zero(len(machine.joltage.jolts)), machine.switches),
        lambda n: n.branches(),
    )
    for node in tree:
        all_equal = True
        for i, j in enumerate(node.state.jolts):
            ref = machine.joltage.jolts[i]
            if j > machine.joltage.jolts[i]:
                tree.dont_descend_into_current_node()
                all_equal = False
                break
            if j != ref:
                all_equal = False
                break
        # print(f"{node.history} => {node.state} for {machine.joltage}")
        if all_equal:
            print(f"[{tree.nodes_visited}] Reached state {node.state} after pressing {sum(node.history)} buttons: {node.history}")
            total_presses += sum(node.history)
            break

print(total_presses)
print(f"Runtime: {time.time()-start_time:.3f} seconds")
