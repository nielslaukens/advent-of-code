import dataclasses

import numpy as np

from tools.tree import traverse_breath_first, for_sendable_generator
from tools.flood_fill import adjacent_positions

GRID_SIZE = 70+1, 70+1
START_POS = 0, 0
END_POS = GRID_SIZE[0]-1, GRID_SIZE[1]-1
falling_bytes: list[tuple[int, int]] = []
with open("input.txt", "r") as f:
    for line in f:
        line = line.strip()
        x, y = line.split(',')
        falling_bytes.append((int(x), int(y)))

print(falling_bytes)
memory = np.full(GRID_SIZE, '.')
#print(memory.transpose())

for falling_byte in falling_bytes[0:1024]:
    memory[falling_byte] = '#'
    #print(memory.transpose())
print(memory.transpose())


@dataclasses.dataclass
class State:
    current_pos: tuple[int, int]
    cost: int
    _visited: list[tuple[int, int]] = None

    def __post_init__(self):
        if self._visited is None:
            self._visited = [self.current_pos]

    def branches(self) -> list["State"]:
        b = []
        for next_pos in adjacent_positions(self.current_pos):
            if not (0 <= next_pos[0] < GRID_SIZE[0] and 0 <= next_pos[1] < GRID_SIZE[1]):
                # out of bounds
                continue
            if next_pos in self._visited:
                continue
            if memory[next_pos] == '#':
                # corrupt
                continue
            b.append(State(next_pos, self.cost+1, [*self._visited, next_pos]))
        return b


it = for_sendable_generator(traverse_breath_first(
    State(START_POS, 0),
    lambda s: s.branches()
))
best_cost_for_position = np.full(GRID_SIZE, None)
for path in it:
    #print(path._visited)
    best_path_for_this_position = best_cost_for_position[path.current_pos]
    if best_path_for_this_position is not None and path.cost >= best_path_for_this_position.cost:
        it.send(True)
    best_cost_for_position[path.current_pos] = path
    if path.current_pos == END_POS:
        # we're exploring breath-first with a constant cost per hop
        # the first node we'll reach will be the shortest
        #print(f"end reached via: {path}")
        break

print(path)
