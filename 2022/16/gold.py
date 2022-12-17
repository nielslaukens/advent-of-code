from __future__ import annotations

import functools
import re
import time
from copy import copy

import typing

from tools import tree_pruning
from tools.graph import dijkstra
from tools.tree_pruning import Tree, Leaf

OPEN_VALVE = 'OPEN_VALVE'
MAX_TIME = 26

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


class DirectedGraph:
    def __init__(self, edge_costs: dict[tuple[typing.Hashable, typing.Hashable], int]):
        self.edge_costs = edge_costs
        self.outbound_edges: dict[typing.Hashable, list[typing.Hashable]] = {}
        self.inbound_edges: dict[typing.Hashable, list[typing.Hashable]] = {}

        for src, dst in self.edge_costs.keys():
            self.outbound_edges.setdefault(src, []).append(dst)
            self.inbound_edges.setdefault(dst, []).append(src)

        self._routes: dict[typing.Hashable, typing.Mapping[typing.Hashable, dijkstra.NextHop]] = {}

    def routes(self, dst: typing.Hashable) -> typing.Mapping[typing.Hashable, dijkstra.NextHop]:
        if dst not in self._routes:
            self._routes[dst] = dijkstra.dijkstra(
                edge_costs=self.edge_costs,
                node_to_calculate_to=dst,
            )
        return self._routes[dst]

    def find_best_path(self, src: typing.Hashable, dst: typing.Hashable) -> list[typing.Hashable]:
        """
        Find path from src to dst.
        Returns a list of next_hop's to take.
        The list includes dst, unless dst == src. That way, len() gives the number of hops
        """
        if src == dst:
            return []

        routes = self.routes(dst)
        path = []
        p = src
        while p != dst:
            p = routes[p].next_hop
            path.append(p)
        return path


edge_costs = {}
for src, dsts in edges.items():
    for dst in dsts:
        edge_costs[(src, dst)] = 1
tunnel_network = DirectedGraph(edge_costs)

useful_valves = []
for valve, flow in valve_flow_rate.items():
    if flow > 0:
        useful_valves.append(valve)


class DoubleOpen(Exception):
    pass


class ChosenPath:
    def __init__(self, actions: list[tuple[str, str]] = None):
        if actions is None:
            actions = []
        self.actions = actions
        self._position = None
        self._previous_positions_since_last_open = None
        self._open_valves = None
        self._current_flow_rate = None
        self._pressure_relieved_so_far = None

    @property
    def time_available(self) -> int:
        a = 0
        while a < MAX_TIME and (
                self.actions[MAX_TIME - a - 1][0] is None
                or self.actions[MAX_TIME - a - 1][1] is None
        ):
            a += 1
        return a

    @property
    def position(self) -> tuple[str, str]:
        if self._position is None:
            self._calculate_state()
        return self._position

    @property
    def previous_positions_since_last_open(self) -> set[str, str]:
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
        self._position = ('AA', 'AA')
        self._previous_positions_since_last_open = (set(), set())
        self._open_valves = set()
        self._current_flow_rate = 0
        self._pressure_relieved_so_far = 0

        for i, action in enumerate(self.actions):
            self._calculate_state_single_step(action, verbose, i)

    def _calculate_state_single_step(self, action: tuple[str, str], verbose: bool = False, t: int = None) -> None:
        self._pressure_relieved_so_far += self._current_flow_rate

        if verbose:
            print()
            print(f"t={t+1} open {self.open_valves}; flow {self.current_flow_rate}; total {self.pressure_relieved}")

        for player in [0, 1]:
            if action[player] is None:
                pass
            elif action[player] == OPEN_VALVE:
                if verbose:
                    print(f"t={t+1} P{player} Opening {self._position[player]} ({valve_flow_rate[self._position[player]]}).")
                if self._position[player] in self._open_valves:
                    raise DoubleOpen(f"Valve {self._position[player]} already open")
                self._open_valves.add(self._position[player])
                self._current_flow_rate += valve_flow_rate[self._position[player]]

                temp = list(self._previous_positions_since_last_open)
                temp[player] = set()
                self._previous_positions_since_last_open = tuple(temp)
            else:
                if verbose:
                    print(f"t={t+1} P{player} Moving to {action[player]}.")
                assert action[player] in edges[self._position[player]]
                self._previous_positions_since_last_open[player].add(self._position[player])

                temp = list(self._position)
                temp[player] = action[player]
                self._position = tuple(temp)

    def do_action(self, action: tuple[str, str]) -> ChosenPath:
        p = ChosenPath([*self.actions, action])

        if self._current_flow_rate is None:
            self._calculate_state()

        # Optimise by re-using current state and only calculating one step ahead
        p._position = self._position
        p._previous_positions_since_last_open = copy(self._previous_positions_since_last_open)
        p._open_valves = copy(self._open_valves)
        p._current_flow_rate = self._current_flow_rate
        p._pressure_relieved_so_far = self._pressure_relieved_so_far
        p._calculate_state_single_step(action)

        return p


class ChosenValveOrder(tree_pruning.Tree):
    def __init__(self, open_valves: list[str]):
        self.open_valves = open_valves
        self.closed_valves = sorted(set(useful_valves).difference(open_valves),
                                    key=lambda valve: valve_flow_rate[valve],
                                    reverse=True)
        # Try high-yield valves first. We'll have to search everything anyway,
        # but this will allow us to prune more/faster

    def __copy__(self) -> ChosenValveOrder:
        return ChosenValveOrder(copy(self.open_valves))

    def branches(self) -> typing.Iterable[tuple[typing.Any, Tree], None, None]:
        # Next steps:
        #  - stop here
        #  - Open up any of the remaining closed valves

        p = self.detailed_pair_steps()
        print(f"Leaf: pr={p.pressure_relieved} by doing ({len(p.actions)}): {p.actions}")
        yield '', Leaf(p.pressure_relieved)

        if p.actions[MAX_TIME-1][0] is not None \
                and p.actions[MAX_TIME-1][1] is not None:
            # time is up, no need to try opening more valves
            return

        for valve in self.closed_valves:
            o = copy(self)
            o.open_valves.append(valve)
            o.closed_valves.remove(valve)
            yield valve, o

    @functools.lru_cache(maxsize=1)
    def detailed_pair_steps(self):
        detailed_steps0 = self.detailed_steps(self.open_valves[0::2])  # even numbered valves
        detailed_steps1 = self.detailed_steps(self.open_valves[1::2])  # odd numbered valves
        p = ChosenPath()
        for i in range(MAX_TIME):
            try:
                s0 = detailed_steps0[i]
            except IndexError:
                s0 = None
            try:
                s1 = detailed_steps1[i]
            except IndexError:
                s1 = None
            p = p.do_action((s0, s1))
        return p

    def detailed_steps(self, valves: list[str]) -> list[str]:
        p = ChosenPath()
        for valve in valves:
            path_to_next = tunnel_network.find_best_path(p.position[0], valve)
            for step in path_to_next:
                p = p.do_action((step, None))
            p = p.do_action((OPEN_VALVE, None))
        return [
            a[0]
            for a in p.actions
        ]

    def score_guaranteed_below(self, score: int) -> bool:
        p = self.detailed_pair_steps()
        time_available = p.time_available
        to_open_in_order = sorted(self.closed_valves, key=lambda valve: valve_flow_rate[valve], reverse=True)
        relieve_potential = 0
        for valve0, valve1 in zip(*[iter(to_open_in_order)]*2):
            relieve_potential += time_available * (valve_flow_rate[valve0] + valve_flow_rate[valve1])
            time_available -= 2  # 1 minute to open this valve, 1 minute to move to the next one (best case)
            if time_available <= 0:
                break
        max_attainable_relieve = p.pressure_relieved + relieve_potential
        if max_attainable_relieve < score:
            return True
        return False


t0 = time.time()
p = ChosenValveOrder([])
path, score = p.search_best_leaf()
print(path)
print(score)
print(time.time() - t0)
