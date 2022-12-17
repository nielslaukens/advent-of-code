from __future__ import annotations

import math
import numbers
import re
import time
import typing

from tools import graph
from tools.graph.floyd_warshall import floyd_warshall
from tools.tree_pruning import Tree

MAX_TIME = 26

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

        self._time = None
        self._position = None
        self._relieved_at_end = None

    def time_relieved(self) -> tuple[list[int], int]:
        if self._time is None:
            # Valves are opened alternating by player 0 (me) and player 1 (elephant)
            self._time = [0, 0]
            self._relieved_at_end = 0
            self._position = ['AA', 'AA']
            for i, v in enumerate(self.open_valves):
                self._add_single_valve(i, v)

        return self._time, self._relieved_at_end

    def _add_single_valve(self, valve_number: int, valve: str) -> None:
        player = valve_number % 2
        self._time[player] += choice_costs[self._position[player]][valve]
        self._position[player] = valve
        time_remaining = MAX_TIME - self._time[player]
        if time_remaining > 0:
            self._relieved_at_end += time_remaining * valve_flow_rate[valve]

    def do_open_valve(self, valve) -> ChosenPath:
        t = ChosenPath([*self.open_valves, valve])
        t._time = [*self._time]
        t._position = [*self._position]
        t._relieved_at_end = self._relieved_at_end
        t._add_single_valve(len(t.open_valves)-1, valve)
        return t

    def branches(self) -> typing.Collection[tuple[typing.Any, Tree], None, None]:
        o = []
        for valve in self.closed_valves:
            t = self.do_open_valve(valve)
            o.append((valve, t))
        return o

    def search_best_leaf(
            self, better_than: numbers.Real = -math.inf,
            _progress: list[float] = None,
    ) -> tuple[list[typing.Any] | None, numbers.Real | None]:
        time, relieved = self.time_relieved()
        if min(time) >= MAX_TIME or len(self.closed_valves) == 0:
            # print(f"{self.open_valves}  => {relieved}")
            return [], relieved

        # else:  # search branches
        return super().search_best_leaf(better_than, _progress=_progress)

    def score_guaranteed_below(self, score: int) -> bool:
        # What if we would turn on all remaining valves
        # We need to move to the valves (at least 1 minute) and turn it on (1 minute)
        # Upper bound: turn on everything at t+2
        time, current_relieve = self.time_relieved()
        time_remaining = MAX_TIME - min(time) - 2
        if time_remaining <= 0:
            # No time to turn on anything anymore
            return current_relieve < score

        remaining_flow = 0
        for valve in self.closed_valves:
            remaining_flow += valve_flow_rate[valve]
        remaining_relieve = remaining_flow * time_remaining
        max_potential = current_relieve + remaining_relieve
        return max_potential < score


t0 = time.time()
p = ChosenPath()
p.time_relieved()
best = p.search_best_leaf()
print(best)
print(time.time() - t0)
