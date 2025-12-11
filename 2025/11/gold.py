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

class Node:
    def __init__(self, path: list[str] = None):
        if path is None:
            path = ["svr"]
        self.path = path

    def __str__(self) -> str:
        return f"Node({self.path})"

    def branches(self) -> typing.Generator[Node, None, None]:
        current_node = self.path[-1]
        for output in device_outputs.get(current_node, []):
            if output in self.path:
                raise RuntimeError(f"Node {current_node} has multiple outputs")
            yield Node([*self.path, output])

tree = tools.tree.TraverseTreeDepthFirstPre(
    Node(),
    lambda n: n.branches(),
)
paths_to_out = 0
for node in tree:
    if tree.nodes_visited % 1_000_000 == 0:
        print(node)
    if node.path[-1] == "out":
        if "fft" in node.path and "dac" in node.path:
            paths_to_out += 1

print(paths_to_out)
