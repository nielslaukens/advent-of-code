from __future__ import annotations

import dataclasses
import math
import typing

import numpy as np

from tools.flood_fill import nested_array_func, adjacent_positions
from tools.tree import TraverseTreeBreathFirst
from tools.tuple_tools import positions_within_distance, manhattan_distance, index_in_range

MAX_CHEAT = 20
MIN_SAVING = 100
with open("input.txt", "r") as f:
    grid = [
        list(line.strip())
        for line in f
    ]


start_pos = None
end_pos = None
for y, row in enumerate(grid):
    for x, ch in enumerate(row):
        if ch == "S":
            start_pos = (y, x)
            assert nested_array_func(grid)(start_pos) == 'S'
            grid[y][x] = "."
        elif ch == "E":
            end_pos = (y, x)
            assert nested_array_func(grid)(end_pos) == 'E'
            grid[y][x] = "."
assert start_pos
assert end_pos


@dataclasses.dataclass
class State:
    pos: tuple[int, int]
    cost: int

    def branches(self) -> typing.Generator[State, None, None]:
        for pos in adjacent_positions(self.pos):
            if nested_array_func(grid)(pos) == '.':
                yield State(pos, self.cost+1)


cost_map = np.full((len(grid), len(grid[0])), fill_value=None)
it = TraverseTreeBreathFirst(State(start_pos, 0), lambda s: s.branches())
for node in it:
    try:
        best_cost_to_beat = cost_map[node.pos].cost
    except AttributeError:
        best_cost_to_beat = math.inf
    if node.cost < best_cost_to_beat:
        cost_map[node.pos] = node
    else:
        it.dont_descend_into_current_node()

for y in range(len(grid)):
    for x in range(len(grid[0])):
        c = cost_map[y][x]
        if c is None:
            c = '---'
        else:
            c = format(c.cost, " 3d")
        print(f"{c} ", end='')
    print()
print()
normal_cost_to_end = cost_map[end_pos].cost
print(f"Normal cost: {normal_cost_to_end}")


# we only need to know how *many* cheats there are and their savings (to filter >=100)
# We don't need to know the path(s) themselves


def cheats_from(pos: tuple[int, int]) -> dict[int, int]:
    if nested_array_func(grid)(pos) != ".":
        # cheats must start on track, so ignore this
        return {}
    cheats = {}
    for reachable_pos in positions_within_distance(pos, MAX_CHEAT):
        if not index_in_range(reachable_pos, cost_map.shape):
            continue
        if nested_array_func(grid)(reachable_pos) != '.':
            # we can only exit on track
            continue
        normal_cost_to_reachable_pos = cost_map[reachable_pos].cost
        d = manhattan_distance(pos, reachable_pos)
        cost_via_cheat_to_reachable_pos = cost_map[pos].cost + d
        if cost_via_cheat_to_reachable_pos < normal_cost_to_reachable_pos:
            savings = normal_cost_to_reachable_pos - cost_via_cheat_to_reachable_pos
            # print(f"Found cheat {pos} -> {reachable_pos} saving "
            #       f"{normal_cost_to_reachable_pos} - {cost_via_cheat_to_reachable_pos} = "
            #       f"{savings}")
            cheats.setdefault(savings, 0)
            cheats[savings] += 1
    return cheats


cheats = {}
for y in range(len(grid)):
    print(f"  calculating {y=}/{len(grid)}")
    for x in range(len(grid[0])):
        pos = (y, x)
        savings_from_pos = cheats_from(pos)
        for shorter, cheats_from_pos in savings_from_pos.items():
            cheats.setdefault(shorter, 0)
            cheats[shorter] += cheats_from_pos

at_least_saving = 0
for save in sorted(cheats.keys()):
    print(f"{cheats[save]} cheats that save {save}")
    if save >= MIN_SAVING:
        at_least_saving += cheats[save]

print(at_least_saving)
