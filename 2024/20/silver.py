from __future__ import annotations

import dataclasses
import math
import typing

import numpy as np

from tools.flood_fill import nested_array_func, adjacent_positions
from tools.tree import TraverseTreeBreathFirst

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
normal_cost = cost_map[end_pos].cost

cheats = {}
for y in range(len(grid)):
    for x in range(len(grid[0])):
        pos = (y, x)
        if cost_map[pos] is None:
            continue
        # else:
        # what cheats are available here?
        for cheat_start in adjacent_positions(pos):
            try:
                grid_at_cheat_start = nested_array_func(grid)(cheat_start)
            except IndexError:  # outside grid
                continue

            if grid_at_cheat_start == '.':
                # We'll get there with cost 1 anyway, no cheat
                continue
            # else:
            assert grid_at_cheat_start == '#'
            for cheat_exit in adjacent_positions(cheat_start):
                if cheat_exit == pos:
                    # no use exiting where we came from
                    continue

                try:
                    grid_at_cheat_exit = nested_array_func(grid)(cheat_exit)
                except IndexError:  # outside grid
                    continue

                if grid_at_cheat_exit == '#':
                    # 2 walls in a row, not a cheat
                    continue
                assert grid_at_cheat_exit == '.'
                cost_to_beat = cost_map[cheat_exit].cost
                cost_by_cheating = cost_map[pos].cost + 2
                if cost_by_cheating < cost_to_beat:
                    cost_saving = cost_to_beat - cost_by_cheating
                    print(f"Found cheat: {cheat_start} -> {cheat_exit}; cost: "
                          f"{normal_cost} - {cost_saving} = {normal_cost-cost_saving}")
                    cheats.setdefault(cost_saving, 0)
                    cheats[cost_saving] += 1

at_least_100_saving = 0
for save in sorted(cheats.keys()):
    print(f"{cheats[save]} cheats that save {save}")
    if save >= 100:
        at_least_100_saving += cheats[save]

print(at_least_100_saving)
