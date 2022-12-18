from __future__ import annotations
from copy import copy

import numpy as np

from tools import numpy_tools

#NUM_BLOCKS = 2022
NUM_BLOCKS = 1_000_000_000_000

with open("input.txt", "r") as f:
    lines = f.readlines()
    assert len(lines) == 1
    jet_directions = list(lines[0].rstrip())

blocks = [
    np.array([
        [1, 1, 1, 1]
    ]),
    np.array([
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0],
    ]),
    np.array([
        [0, 0, 1],
        [0, 0, 1],
        [1, 1, 1],
    ]),
    np.array([
        [1],
        [1],
        [1],
        [1],
    ]),
    np.array([
        [1, 1],
        [1, 1],
    ])
]
blocks = [
    np.flip(block, axis=0)  # numpy array of chamber is upside-down (y toward top)
    for block in blocks
]


class Cycle:
    # Similar to itertools.cycle(), but with diagnostics
    def __init__(self, to_cycle: list):
        self.list = to_cycle
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        i = self.i
        self.i = (self.i + 1) % len(self.list)
        return self.list[i]


blocks_iter = Cycle(blocks)
jet_iter = Cycle(jet_directions)


class Collision(Exception):
    pass


class Chamber:
    def __init__(self, rock_iter, jet_iter):
        self.chamber = np.full(shape=(1, 7), dtype="<U1", fill_value='#')
        self.chamber_bottom_y = 0
        self.rock_iter = rock_iter
        self.jet_iter = jet_iter
        self.rocks = 0

    def __copy__(self) -> Chamber:
        c = Chamber(None, None)
        c.chamber = np.copy(self.chamber)
        c.chamber_bottom_y = self.chamber_bottom_y
        return c

    def print_chamber(self) -> None:
        # Chamber is indexed (y, x)
        # x measures to the right
        # y measures to the top => flip axis 0 and print
        flipped = np.flip(self.chamber, axis=0)
        print(numpy_tools.str_values_only(flipped))
        print(f"..{self.chamber_bottom_y} more..")
        print()

    def top_of_stack(self) -> int:
        for y in range(self.chamber.shape[0]-1, 0-1, -1):
            if not np.all(self.chamber[y, :] == '.'):
                return y + self.chamber_bottom_y
        return 0

    def _extend_chamber(self, top: int):
        if top <= self.chamber_bottom_y + self.chamber.shape[0]:
            return
        self.chamber = np.vstack([
            self.chamber,
            np.full(shape=(top - self.chamber_bottom_y - self.chamber.shape[0],
                           self.chamber.shape[1]),
                    fill_value='.')
        ])

    def find_seal(self) -> int:
        # Scan top to bottom for a series of N rows that seal left to right
        # For N=1, it's obvious that nothing can pass
        # For N=2: to pass, you need a gap to zig-zag through, which isn't there:
        #    |#...##.|
        #    |.###..#|
        #
        # For N=3: the least-tall block is the "-" one. Our chamber isn't wide enough to pass
        # |###@@@@|
        # |.......|
        # |...####|
        N = 3
        for y in range(self.chamber.shape[0]-N, N-2, -1):
            all_x_sealed = True
            for x in range(self.chamber.shape[1]):
                this_x_sealed = False
                for dy in range(N):
                    if self.chamber[y + dy, x] != '.':
                        this_x_sealed = True
                        break
                if not this_x_sealed:
                    all_x_sealed = False
                    break
            if all_x_sealed:
                break
        else:
            return 0
        return y

    def is_valid(self, rock: np.ndarray, new_pos: tuple[int, int]) -> bool:
        if new_pos[1] < 0:  # hit left wall
            return False
        try:
            _ = self.overlayed(rock, new_pos, find_seal=False)  # may raise
            return True
        except (Collision, IndexError):
            return False

    def overlayed(
            self,
            rock: np.ndarray,
            rock_lb_pos: tuple[int, int],
            symbol: str = '@',
            find_seal: bool = True,
    ) -> np.ndarray:
        ch = copy(self)
        ch.overlay(rock, rock_lb_pos, symbol, find_seal)
        return ch.chamber

    def overlay(
            self,
            rock: np.ndarray,
            rock_lb_pos: tuple[int, int],
            symbol: str = '#',
            find_seal: bool = True,
    ) -> None:
        self._extend_chamber(rock_lb_pos[0] + rock.shape[0])

        it = np.nditer(rock, flags=['multi_index'])
        for block_or_empty in it:
            y, x = it.multi_index
            if block_or_empty == 1:
                coord = (y + rock_lb_pos[0] - self.chamber_bottom_y), (x + rock_lb_pos[1])
                if self.chamber[coord] != '.':
                    raise Collision()
                self.chamber[coord] = symbol

        if find_seal:
            seal_at = self.find_seal()
            if seal_at > 0:
                self.chamber_bottom_y += seal_at
                self.chamber = self.chamber[seal_at:, :]

    def state(self) -> tuple[int]:
        all_int = []
        for y in range(self.chamber.shape[0]):
            x_int = 0
            for x in range(self.chamber.shape[1]):
                 x_int += (0 if self.chamber[y, x] == '.' else 1) * 2**x
            all_int.append(x_int)
        return tuple(all_int)

    def do_rock(self) -> None:
        self.rocks += 1
        falling_rock = next(self.rock_iter)
        rock_lb_pos = (self.top_of_stack() + 1 + 3, 2)  # (y, x)

        #print(self.overlayed(falling_rock, rock_lb_pos))
        try:
            while True:  # until Collision() exception
                jet_direction = next(self.jet_iter)
                #print(jet_direction)
                if jet_direction == '>':
                    new_pos = (rock_lb_pos[0], rock_lb_pos[1]+1)
                elif jet_direction == '<':
                    new_pos = (rock_lb_pos[0], rock_lb_pos[1]-1)
                else:
                    raise ValueError(jet_direction)
                if self.is_valid(falling_rock, new_pos):
                    rock_lb_pos = new_pos
                #print(c.overlayed(falling_rock, rock_lb_pos))

                # drop
                new_pos = (rock_lb_pos[0] - 1, rock_lb_pos[1])
                _ = self.overlayed(falling_rock, new_pos, find_seal=False)  # may raise
                rock_lb_pos = new_pos
                #print(_)
        except Collision:
            pass

        self.overlay(falling_rock, rock_lb_pos)
        #print(f"After rock {self.rocks}:")
        #self.print_chamber()
        #print(f"rock={blocks_iter.i}, jet={jet_iter.i}, ch={c.state()}")


c = Chamber(blocks_iter, jet_iter)
seen_states = {}
while True:  # Until cycle
    c.do_rock()

    s = (blocks_iter.i, jet_iter.i, c.state())
    if s in seen_states:
        break
    else:
        seen_states[s] = (c.rocks, c.chamber_bottom_y)

assert s in seen_states
assert c.rocks < NUM_BLOCKS
print(f"After rock {c.rocks}, we are in the same state as after rock {seen_states[s][0]}")
rocks_per_cycle = c.rocks - seen_states[s][0]
extra_height_per_cycle = c.chamber_bottom_y - seen_states[s][1]
print(f"We moved up {extra_height_per_cycle} during that {rocks_per_cycle} rock cycle")

# fast-forward to the end
# c.rocks + N * rocks_per_cycle + rest = NUM_BLOCKS
# NUM_BLOCKS - c.rocks = N * rocks_per_cycle + rest
# N = (NUM_BLOCKS - c.rocks) // rocks_per_cycle
cycles = (NUM_BLOCKS - c.rocks) // rocks_per_cycle
c.rocks += cycles * rocks_per_cycle
c.chamber_bottom_y += cycles * extra_height_per_cycle

# do the final series
while c.rocks < NUM_BLOCKS:
    c.do_rock()

print(c.top_of_stack())
