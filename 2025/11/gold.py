from __future__ import annotations
import typing
from pprint import pprint

import tools.tree

device_outputs = {}
with open("input.txt") as f:
    for line in f.read().splitlines():
        device, outputs = line.split(': ')
        device_outputs[device] = outputs.split(' ')
#pprint(device_outputs)

# Normal tree search with validation is too slow...
# Let's see if we can reverse the problem: work from out back towards svr
device_inputs = {}
for device, outputs in device_outputs.items():
    for output in outputs:
        device_inputs.setdefault(output, []).append(device)
pprint(device_inputs)

class Node:
    def __init__(self, path: list[str]):
        self.path = path

    def __str__(self) -> str:
        return f"Node({self.path})"

    def branches(self) -> typing.Generator[Node, None, None]:
        current_node = self.path[-1]
        for output in device_inputs.get(current_node, []):
            if output in self.path:
                raise RuntimeError(f"loop")
            yield Node([*self.path, output])


def find_num_paths_between(a: str, b: str) -> int:
    tree = tools.tree.TraverseTreeBreathFirst(
        Node([b]),
        lambda n: n.branches(),
    )
    paths = 0
    for node in tree:
        if tree.nodes_visited % 1_000_000 == 0:
            print(node)
        if node.path[-1] == a:
            paths += 1
    return paths

fft_dac_1 = find_num_paths_between("svr", "fft")
fft_dac_2 = find_num_paths_between("fft", "dac")
fft_dac_3 = find_num_paths_between("dac", "out")
fft_dac = fft_dac_1 * fft_dac_2 * fft_dac_3
print(fft_dac_1, fft_dac_2, fft_dac_3, "=", fft_dac)

dac_fft_1 = find_num_paths_between("svr", "dac")
dac_fft_2 = find_num_paths_between("dac", "fft")
dac_fft_3 = find_num_paths_between("fft", "out")
dac_fft = dac_fft_1 * dac_fft_2 * dac_fft_3
print(dac_fft_1, dac_fft_2, dac_fft_3, "=", dac_fft)

print(fft_dac + dac_fft)
