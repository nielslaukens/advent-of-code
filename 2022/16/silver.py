from __future__ import annotations

import functools
import math
import numbers
import re
import typing

from tools import graph
from tools.graph.floyd_warshall import floyd_warshall
from tools.tree_pruning import Tree

MAX_TIME = 30

valve_flow_rate: dict[str, int] = {}
outbound_tunnels: dict[str, list[str]] = {}

with open("input.txt", "r") as f:
    for line in f:
        match = re.match(r'Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)', line)
        if not match:
            raise ValueError(f"Didn't understand: {line}")

        node = match.group(1)
        node_rate = int(match.group(2))
        tunnels = [
            _.strip()
            for _ in match.group(3).split(',')
        ]

        valve_flow_rate[node] = node_rate
        outbound_tunnels[node] = tunnels

tunnel_edge_costs = {}
for position, out in outbound_tunnels.items():
    for dst in out:
        tunnel_edge_costs[(position, dst)] = 1  # takes 1 minute to traverse

# Remove useless intermediary nodes where no (useful) valve is located
useful_valves = set()
for valve, flow in valve_flow_rate.items():
    if flow == 0 and valve != 'AA':
        tunnel_edge_costs = graph.remove_node(tunnel_edge_costs, valve, reconnect_edges=True)
    if flow > 0:
        useful_valves.add(valve)

# Calculate travel time between any 2 nodes. Then add 1 minute to open the valve at the destination.
# There is no use to travel to a valve when you're not opening it
choice_costs = floyd_warshall(tunnel_edge_costs)
for src, _ in choice_costs.items():
    del _[src]  # remove traveling to self
    for dst, cost in _.items():
        _[dst] += 1


class ChosenPath(Tree):
    def __init__(self, open_valves: list[str] = None):
        if open_valves is None:
            open_valves = []
        self.open_valves = open_valves
        self.closed_valves = useful_valves.difference(self.open_valves)

    def time_relieved(self) -> tuple[int, int]:
        time = 0
        relieved_at_end = 0
        current_position = 'AA'
        for v in self.open_valves:
            time += choice_costs[current_position][v]
            current_position = v
            time_remaining = MAX_TIME - time
            if time_remaining > 0:
                relieved_at_end += time_remaining * valve_flow_rate[v]
        return time, relieved_at_end

    def branches(self) -> typing.Iterable[tuple[typing.Any, Tree], None, None]:
        for valve in self.closed_valves:
            t = ChosenPath([*self.open_valves, valve])
            yield valve, t

    def search_best_leaf(
            self, better_than: numbers.Real = -math.inf
    ) -> tuple[list[typing.Any] | None, numbers.Real | None]:
        time, relieved = self.time_relieved()
        if time >= MAX_TIME or len(self.closed_valves) == 0:
            #print(f"{self.open_valves}  => {relieved}")
            return [], relieved

        # else:  # search branches
        return super().search_best_leaf(better_than)


p = ChosenPath()
best = p.search_best_leaf()
print(best)
