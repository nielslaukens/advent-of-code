from __future__ import annotations
import dataclasses
import re
import typing
import time
from pprint import pprint

import tools.tree

start_time = time.time()

class Lights:
    """
    Store light status as integer, little endian (i.e. bit 0 represents the first light, bit 1 the second light, ...)
    """
    def __init__(self, length: int):
        self._num_lights = length
        self._lights = 0

    @classmethod
    def from_string(cls, status: str):
        obj = cls(len(status))
        for i, ch in enumerate(status):
            obj._lights |= (1 if ch == '#' else 0) * (1<<i)
        return obj

    @property
    def num_lights(self) -> int:
        return self._num_lights

    def __str__(self) -> str:
        s = ''
        for i in range(self._num_lights):
            s += '#' if self._lights & (1<<i) else '.'
        return s

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(str(self))})"

    def __eq__(self, other: typing.Any) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self._num_lights == other._num_lights and self._lights == other._lights

    def off(self) -> Lights:
        return Lights(self._num_lights)

    def toggle(self, lights: list[int]) -> Lights:
        flip = 0
        for light in lights:
            if light < 0 or light >= self._num_lights:
                raise ValueError('light index out of range')
            flip |= 1<<light
        o = Lights(self._num_lights)
        o._lights = self._lights ^ flip
        return o


l = Lights.from_string('....')
l = l.toggle([0, 1, 3])
assert str(l) == "##.#"
l = l.toggle([0, 2])
assert str(l) == ".###"


@dataclasses.dataclass
class Machine:
    lights: Lights
    switches: list[list[int]]
    joltage: list[int]


machines = []
with open("input.txt") as f:
    for line in f:
        line = line.rstrip()
        m = re.fullmatch(r'\[([.#]+)] ([^{]+){(.*)}', line)
        lights = Lights.from_string(m.group(1))
        switches = m.group(2)[1:-2]  # strip starting '(' and ending ') '
        switches = [[int(pos) for pos in switch.split(',')] for switch in switches.split(') (')]
        joltage = [int(num) for num in m.group(3).split(',')]
        machines.append(Machine(lights, switches, joltage))


class ButtonPresses:
    def __init__(self, lights: Lights, options: list[list[int]], history: list[int] = None):
        if history is None:
            history = []
        self.state = lights
        self.options = options
        self.history = history

    def branches(self) -> typing.Generator[ButtonPresses, None, None]:
        for i, t in enumerate(self.options):
            l = self.state.toggle(t)
            yield ButtonPresses(l, self.options, [*self.history, i])

    def __str__(self) -> str:
        return f"{self.state} after {self.history}"


total_presses = 0
for machine in machines:
    pprint(machine)

    tree = tools.tree.TraverseTreeBreathFirst(
        ButtonPresses(Lights(machine.lights.num_lights), machine.switches),
        lambda n: n.branches(),
    )
    for node in tree:
        if node.state == machine.lights:
            print(f"Reached state {node.state} after pressing {len(node.history)} buttons: {node.history}")
            total_presses += len(node.history)
            break

print(total_presses)
print(f"Runtime: {time.time()-start_time:.3f} seconds")
