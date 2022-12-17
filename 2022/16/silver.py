from __future__ import annotations

import re
import time
from copy import copy

import typing

from tools import graph

OPEN_VALVE = 'OPEN_VALVE'
MAX_TIME = 30

valve_flow_rate: dict[str, int] = {}
edges: dict[str, list[str]] = {}

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
        edges[node] = tunnels


class ChosenPath(graph.Node):
    def __init__(self, actions: list[str]):
        self.actions = actions
        self._position = None
        self._previous_positions_since_last_open = None
        self._open_valves = None
        self._current_flow_rate = None
        self._pressure_relieved_so_far = None

    @property
    def time(self) -> int:
        return len(self.actions)

    @property
    def position(self) -> str:
        if self._position is None:
            self._calculate_state()
        return self._position

    @property
    def previous_positions_since_last_open(self) -> str:
        if self._previous_positions_since_last_open is None:
            self._calculate_state()
        return self._previous_positions_since_last_open

    @property
    def open_valves(self) -> set[str]:
        if self._open_valves is None:
            self._calculate_state()
        return self._open_valves

    @property
    def current_flow_rate(self) -> int:
        if self._current_flow_rate is None:
            self._calculate_state()
        return self._current_flow_rate

    @property
    def pressure_relieved(self) -> int:
        if self._pressure_relieved_so_far is None:
            self._calculate_state()
        return self._pressure_relieved_so_far

    def print(self):
        self._calculate_state(verbose=True)

    def _calculate_state(self, verbose: bool = False) -> None:
        self._position = 'AA'
        self._previous_positions_since_last_open = set()
        self._open_valves = set()
        self._current_flow_rate = 0
        self._pressure_relieved_so_far = 0

        for i, action in enumerate(self.actions):
            self._calculate_state_single_step(action, verbose, i)

    def _calculate_state_single_step(self, action, verbose: bool = False, t: int = None) -> None:
        self._pressure_relieved_so_far += self._current_flow_rate
        if action == OPEN_VALVE:
            if verbose:
                print(f"t={t+1} Opening {self._position} ({valve_flow_rate[self._position]}). "
                      f"Releasing {self._current_flow_rate}/min. "
                      f"Released so far: {self._pressure_relieved_so_far}. "
                      f"Already open: {self._open_valves}")
            assert self._position not in self._open_valves
            self._open_valves.add(self._position)
            self._current_flow_rate += valve_flow_rate[self._position]
            self._previous_positions_since_last_open = set()
        else:
            if verbose:
                print(f"t={t+1} Moving to {action}. "
                      f"Releasing {self._current_flow_rate}/min. "
                      f"Released so far: {self._pressure_relieved_so_far}. "
                      f"Already open: {self._open_valves}")
            assert action in edges[self._position]
            self._previous_positions_since_last_open.add(self._position)
            self._position = action

    def upper_bound_on_relieved_at_max_time(self) -> int:
        valves_still_closed = set(valve_flow_rate.keys()).difference(self.open_valves)
        valves_still_closed = sorted(list(valves_still_closed), key=lambda name: valve_flow_rate[name], reverse=True)
        time_remaining = MAX_TIME - self.time

        # open valves, highest yield first, 1 minute apart (i.e. instant travel)
        extra_relieved_pressure_at_end = 0
        for i, valve in enumerate(valves_still_closed):
            time_this_valve_can_be_open = (time_remaining - i)
            if time_this_valve_can_be_open <= 0:
                break
            extra_relieved_pressure_at_end += valve_flow_rate[valve] * time_this_valve_can_be_open

        return self.pressure_relieved \
            + self.current_flow_rate * time_remaining \
            + extra_relieved_pressure_at_end

    def outbound_edges(self) -> typing.Generator[ChosenPath, None, None]:
        if self.time >= MAX_TIME:
            return

        global best_path
        if best_path is not None and self.upper_bound_on_relieved_at_max_time() < best_path.pressure_relieved:
            return

        if self.position not in self.open_valves and valve_flow_rate[self.position] > 0:
            yield self.do_action(OPEN_VALVE)

        for towards in edges[self.position]:
            if towards in self.previous_positions_since_last_open:
                # no use to go back to where we came from without doing anything
                continue

            yield self.do_action(towards)

    def do_action(self, action: str) -> ChosenPath:
        p = ChosenPath([*self.actions, action])

        # Optimise by re-using current state and only calculating one step ahead
        p._position = self._position
        p._previous_positions_since_last_open = copy(self._previous_positions_since_last_open)
        p._open_valves = copy(self._open_valves)
        p._current_flow_rate = self._current_flow_rate
        p._pressure_relieved_so_far = self._pressure_relieved_so_far
        p._calculate_state_single_step(action)

        return p


t0 = time.time()
p = ChosenPath([])
best_path = None
for i, path in enumerate(p.recursive_walk(graph.Node.Order.LeafOnly)):
    if best_path is None or path.pressure_relieved > best_path.pressure_relieved:
        best_path = path
    #print(f"path {i}, relieved: {path.pressure_relieved} from {path.actions}")

print(f"Searched {i} paths in {time.time() - t0:.3f} seconds")
print(f"{best_path.pressure_relieved} from {len(best_path.actions)} {best_path.actions}")
#best_path.print()

# 1796  too low
# 1906  OK
