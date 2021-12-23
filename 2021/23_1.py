"""
Not optimal, takes way to long to find the correct answer
Optimizations possible:
 - Don't brute-force the hallway position, but be more intelligent
"""

import copy
import typing


class MoveError(Exception):
    pass


class Puzzle:
    def __init__(
            self,
            hallway: typing.List[typing.Optional[str]],
            chamber_pos: typing.List[int],
            chamber_occupants: typing.List[typing.List[str]],
    ):
        assert len(chamber_pos) == len(chamber_occupants)
        self.hallway = hallway
        self.chamber_pos = chamber_pos
        self.chamber_occupants = chamber_occupants

        self.energy = 0
        self.energy_map = {
            'A': 1,
            'B': 10,
            'C': 100,
            'D': 1000,
        }
        self.steps = []

    @classmethod
    def from_string(cls, s: str) -> "Puzzle":
        lines = s.split('\n')
        assert lines[0] == "#############"
        assert lines[1] == "#...........#"
        #                  "###:#:#:#:###"
        #                  "  #:#:#:#:#"
        assert lines[4] == "  #########"

        return Puzzle(
            hallway=[None] * 11,
            chamber_pos=[2, 4, 6, 8],
            chamber_occupants=[
                [lines[2][3:4], lines[3][3:4]],
                [lines[2][5:6], lines[3][5:6]],
                [lines[2][7:8], lines[3][7:8]],
                [lines[2][9:10], lines[3][9:10]],
            ]
        )

    def __str__(self) -> str:
        o = ""
        for p in self.hallway:
            o += p if p is not None else '.'
        o += "\n"
        for depth in range(2):
            line = ""
            for ch_num, ch_occs in enumerate(self.chamber_occupants):
                line += " " * (self.chamber_pos[ch_num] - len(line))
                occ = ch_occs[depth]
                line += occ if occ is not None else '.'
            o += line + "\n"
        return o

    def copy(self) -> "Puzzle":
        p = Puzzle(
            hallway=copy.deepcopy(self.hallway),
            chamber_pos=self.chamber_pos,
            chamber_occupants=copy.deepcopy(self.chamber_occupants)
        )
        p.energy = self.energy
        p.steps = copy.deepcopy(self.steps)
        return p

    def _hallway_move(self, start: int, end: int, energy_per_step: int) -> "Puzzle":
        assert self.hallway[start] is not None
        if start == end:
            return self

        after = self.copy()

        direction = 1 if end > start else -1
        for horizontal_step in range(start, end, direction):
            if after.hallway[start + direction] is not None:
                raise MoveError(f"Can't pass hallway position {start+direction}, not free")
            after.hallway[start + direction] = after.hallway[start]
            after.hallway[start] = None
            start = start + direction
            after.energy += energy_per_step

        return after

    def exit_from_chamber(self, chamber_num: int, hallway_pos: int) -> "Puzzle":
        for ch_p in self.chamber_pos:
            if hallway_pos == ch_p:
                raise MoveError("Can't stop in front of chamber")

        after = self.copy()

        if after.chamber_occupants[chamber_num][0] is None:
            # top position already empty, move bottom position one up
            after.chamber_occupants[chamber_num][0] = after.chamber_occupants[chamber_num][1]
            after.chamber_occupants[chamber_num][1] = None
            after.energy += after.energy_map[after.chamber_occupants[chamber_num][0]]

        amphipod_type = after.chamber_occupants[chamber_num][0]
        energy_per_step = after.energy_map[amphipod_type]

        # move from chamber exit into hallway
        p = after.chamber_pos[chamber_num]
        after.hallway[p] = after.chamber_occupants[chamber_num][0]
        after.chamber_occupants[chamber_num][0] = None
        after.energy += energy_per_step

        after = after._hallway_move(p, hallway_pos, energy_per_step)
        after.steps.append(f'Exit {amphipod_type} from chamber {chamber_num} ({after.chamber_pos[chamber_num]}) to hallway {hallway_pos}')
        return after

    def enter_chamber(self, hallway_pos: int) -> "Puzzle":
        amphipod_type = self.hallway[hallway_pos]
        if amphipod_type is None:
            raise MoveError(f"No Amphipod in hallway position {hallway_pos}")
        chamber_num = ord(amphipod_type) - ord('A')

        if self.chamber_occupants[chamber_num][0] is not None:
            raise MoveError(f"Can't move into chamber {chamber_num}, not free")
        if self.chamber_occupants[chamber_num][1] is not None and \
                self.chamber_occupants[chamber_num][1] != amphipod_type:
            raise MoveError("Would block wrong amphipod in chamber")

        energy_per_step = self.energy_map[self.hallway[hallway_pos]]
        after = self._hallway_move(hallway_pos, self.chamber_pos[chamber_num], energy_per_step)

        # move down into chamber
        after.chamber_occupants[chamber_num][0] = after.hallway[after.chamber_pos[chamber_num]]
        after.hallway[after.chamber_pos[chamber_num]] = None
        after.energy += energy_per_step

        if after.chamber_occupants[chamber_num][1] is None:
            # move one more down
            after.chamber_occupants[chamber_num][1] = after.chamber_occupants[chamber_num][0]
            after.chamber_occupants[chamber_num][0] = None
            after.energy += energy_per_step

        after.steps.append(f"Enter {amphipod_type} from hallway {hallway_pos} into chamber {chamber_num} ({after.chamber_pos[chamber_num]})")
        return after

    def need_exit(self) -> typing.List[int]:
        e = []
        def check_single_chamber(chamber_num: int, amphipod_type: str):
            if (self.chamber_occupants[chamber_num][0] is not None
                    and self.chamber_occupants[chamber_num][0] != amphipod_type) \
                    or (self.chamber_occupants[chamber_num][1] is not None
                    and self.chamber_occupants[chamber_num][1] != amphipod_type):
                e.append(chamber_num)
        check_single_chamber(0, 'A')
        check_single_chamber(1, 'B')
        check_single_chamber(2, 'C')
        check_single_chamber(3, 'D')
        return e

    def need_entry(self) -> typing.List[int]:
        positions = []
        for p, a_type in enumerate(self.hallway):
            if a_type is not None:
                positions.append(p)
        return positions

    def done(self) -> bool:
        return self.chamber_occupants[0][0] == 'A' and \
            self.chamber_occupants[0][1] == 'A' and \
            self.chamber_occupants[1][0] == 'B' and \
            self.chamber_occupants[1][1] == 'B' and \
            self.chamber_occupants[2][0] == 'C' and \
            self.chamber_occupants[2][1] == 'C' and \
            self.chamber_occupants[3][0] == 'D' and \
            self.chamber_occupants[3][1] == 'D'


with open("23.sample.txt", "r") as f:
    puzzle = Puzzle.from_string(f.read())

# Options are:
#  - What order they exit their cave (if they do)
#  - To what hallway position they move
#  - What order they enter their cave


def try_entry(puzzle: Puzzle) -> Puzzle:
    # always try entry first, so they are out of our way
    while len(puzzle.need_entry()) > 0:
        # Keep trying until everything is in their chamber
        for need_entry in list(puzzle.need_entry()):
            try:
                puzzle = puzzle.enter_chamber(need_entry)
                break  # We could enter one, restart the search to see if we (now) can enter others
            except MoveError:
                pass
        else:
            # No entries could be done, break while loop
            break
    return puzzle


def step(puzzle: Puzzle) -> Puzzle:
    best = None
    for option in set(puzzle.need_exit()):
        for hallway_pos in range(11):
            try:
                puzzle_after_this_option = puzzle.exit_from_chamber(option, hallway_pos)
                puzzle_after_this_option = try_entry(puzzle_after_this_option)
                if not puzzle_after_this_option.done():
                    puzzle_after_this_option = step(puzzle_after_this_option)
                if puzzle_after_this_option is not None:
                    if best is None or puzzle_after_this_option.energy < best.energy:
                        best = puzzle_after_this_option
            except MoveError:
                pass
    return best


print(puzzle)
puzzle = step(puzzle)
print(puzzle)
print(puzzle.energy)
print('\n'.join(puzzle.steps))
