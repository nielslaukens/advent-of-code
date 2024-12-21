from __future__ import annotations

import collections
import itertools
import typing

from tools.tuple_tools import tuple_add

codes: list[str] = []
with open("input.txt", "r") as f:
    for line in f:
        codes.append(line.strip())


class RobotArmPointingAtKeypad:
    def __init__(self, output: collections.abc.Callable[[str], None], name: str, start_pos: tuple[int, int]):
        self.output = output
        self.name = name
        self.start_pos = start_pos

        self.inv_keymap = {}
        for pos, key in self.keymap.items():
            self.inv_keymap[key] = pos

        self.reset()

    def reset(self):
        self.pos = self.start_pos

    def __str__(self) -> str:
        return self.name

    @property
    def key_under_pos(self) -> str:
        return self.keymap.get(self.pos)

    def move(self, direction: str) -> None:
        if direction == '^':
            self.pos = tuple_add(self.pos, (1, 0))
        elif direction == 'v':
            self.pos = tuple_add(self.pos, (-1, 0))
        elif direction == '<':
            self.pos = tuple_add(self.pos, (0, 1))
        elif direction == '>':
            self.pos = tuple_add(self.pos, (0, -1))
        elif direction == 'A':
            pass
        else:
            raise RuntimeError(f'Unknown direction: {direction}')
        if direction == 'A':
            #print(f"{self} {direction} on {self.key_under_pos}")
            self.output(self.key_under_pos)
        else:
            #print(f"{self} {direction} to {self.pos} over {self.key_under_pos}")
            pass
        if self.keymap.get(self.pos) is None:
            raise ValueError(f'{self} is not over key, panic')

    def moves(self, directions: str) -> None:
        for ch in directions:
            self.move(ch)

    def shortest_paths_to_key(self, key: str) -> typing.Generator[str, None, None]:
        return self.shortest_paths_to_pos(self.inv_keymap[key])

    def shortest_paths_to_pos(self, target: tuple[int, int]) -> typing.Generator[str, None, None]:
        # The order we output the operations in, becomes important
        # On the first level, all orders have the same length
        # but due to the stacking of robots, this is no longer the case: e.g.
        #  1. <<^^A would need v<<A, A, >^A, A, >A
        #  2. ^^<<A would need <A, A, v<A, A, >>^A
        # Both require 11 pushes. But one level deeper, these become:
        #  1.1. v<<A: v<A, <A, A, >>^A  (10)
        #  1.2. A: A (1)
        #  1.3. >^A: vA, <^A, >A (7)
        #  1.4. A: A (1)
        #  1.5. >A: vA, ^A (4)
        # totalling 23; while 2 gives:
        #  2.1. <A: v<<A, >>^A  (8)
        #  2.2. A: A  (1)
        #  3.3. v<A: v<A, <A, >>^A  (9)
        #  3.4. A: A  (1)
        #  3.5. >>^A: vA, A, <^A, >A  (8)
        # totalling 27
        #
        # So we'll need to output all possible orders, and do a search through that

        up_down = target[0] - self.pos[0]
        up_down_moves = ('^' if up_down > 0 else 'v') * abs(up_down)
        left_right = target[1] - self.pos[1]
        left_right_moves = ('<' if left_right > 0 else '>') * abs(left_right)

        paths = []
        for moves in itertools.permutations(up_down_moves + left_right_moves):
            # check if we pass over the gap
            try:
                current_pos = self.pos
                self.moves(moves)
                assert self.pos == target
                self.pos = current_pos
                yield ''.join(moves)
            except ValueError:
                # Went over gap, ignore this path
                assert self.keymap[self.pos] is None  # may raise KeyError if key is actually outside map
                self.pos = current_pos


class RobotArmPointingAtNumericKeypad(RobotArmPointingAtKeypad):
    #      [2] [1] [0]   <- coordinates
    #     +---+---+---+
    # [3] | 7 | 8 | 9 |
    #     +---+---+---+
    # [2] | 4 | 5 | 6 |
    #     +---+---+---+
    # [1] | 1 | 2 | 3 |
    #     +---+---+---+
    # [0]     | 0 | A |
    #         +---+---+
    keymap = {
        (3, 2): '7',
        (3, 1): '8',
        (3, 0): '9',
        (2, 2): '4',
        (2, 1): '5',
        (2, 0): '6',
        (1, 2): '1',
        (1, 1): '2',
        (1, 0): '3',
        (0, 2): None,
        (0, 1): '0',
        (0, 0): 'A',
    }

    def __init__(self, output: collections.abc.Callable[[str], None], name: str):
        super().__init__(output, name, (0, 0))


class RobotArmPointingAtRobotKeypad(RobotArmPointingAtKeypad):
    #      [2] [1] [0]   <- coordinates
    #         +---+---+
    # [1]     | ^ | A |
    #     +---+---+---+
    # [0] | < | v | > |
    #     +---+---+---+
    keymap = {
        (1, 2): None,
        (1, 1): '^',
        (1, 0): 'A',
        (0, 2): '<',
        (0, 1): 'v',
        (0, 0): '>',
    }

    def __init__(self, output: collections.abc.Callable[[str], None], name: str):
        super().__init__(output, name, (1, 0))

if False:
    keypad = ''
    def r1_out(d):
        #print(f"{d}")
        global keypad
        keypad += d
    robot1 = RobotArmPointingAtNumericKeypad(output=r1_out, name="_")

    def r2_out(d):
        #print(f"    {d}")
        robot1.move(d)
    robot2 = RobotArmPointingAtRobotKeypad(output=r2_out, name="_____")

    def r3_out(d):
        #print(f"        {d}")
        robot2.move(d)
    robot3 = RobotArmPointingAtRobotKeypad(output=r3_out, name="_________")

    mine = 'v<<A>>^AvA^Av<<A>>^AAv<A<A>>^AAvAA^<A>Av<A>^AA<A>Av<A<A>>^AAAvA^<A>A'
    theirs = '<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A'
    for move in theirs:
        robot3.move(move)
    sys.exit()


def find_shortest_path_length(code: str, robots: list[RobotArmPointingAtKeypad]) -> str:
    assert code.endswith('A')
    #print(code)
    if len(robots) == 0:
        return code
    shortest_all = ''
    for digit in code:
        paths = robots[0].shortest_paths_to_key(digit)
        paths_A = (p + 'A' for p in paths)
        shortest_for_digit = None
        for path in paths_A:
            l = find_shortest_path_length(path, robots[1:])
            if shortest_for_digit is None or len(l) < len(shortest_for_digit):
                shortest_for_digit = l
        robots[0].pos = robots[0].inv_keymap[digit]
        shortest_all += shortest_for_digit
    assert robots[0].key_under_pos == 'A'
    return shortest_all

total_complexity = 0
for code in codes:
    robot3_input = find_shortest_path_length(code, [
        RobotArmPointingAtNumericKeypad(output=lambda d: None, name="_"),
        RobotArmPointingAtRobotKeypad(output=lambda d: None, name="_____"),
        RobotArmPointingAtRobotKeypad(output=lambda d: None, name="_________"),
    ])
    complexity = len(robot3_input) * int(code[:-1])
    print(f"{len(robot3_input)} * {int(code[:-1])} = {complexity}")
    total_complexity += complexity

print(total_complexity)
