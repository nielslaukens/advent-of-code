from __future__ import annotations
import typing
from pprint import pprint

import tools.tree

device_outputs = {}
with open("input.txt") as f:
    for line in f.read().splitlines():
        device, outputs = line.split(': ')
        device_outputs[device] = outputs.split(' ')
pprint(device_outputs)

class Node:
    def __init__(self, path: list[str] = None):
        if path is None:
            path = ["you"]
        self.path = path

    def branches(self) -> typing.Generator[Node, None, None]:
        current_node = self.path[-1]
        for output in device_outputs.get(current_node, []):
            yield Node([*self.path, output])

tree = tools.tree.TraverseTreeDepthFirstPre(
    Node(),
    lambda n: n.branches(),
)
paths_to_out = 0
for node in tree:
    if node.path[-1] == "out":
        paths_to_out += 1

print(paths_to_out)