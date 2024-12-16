import dataclasses
import enum
from functools import cached_property

import numpy as np

from tools.int_tools import tuple_add
from tools.numpy_tools import str_values_only
from tools.tree import traverse_breath_first, for_sendable_generator

with open("input.txt", "r") as f:
    maze = [
        list(line.strip())
        for line in f.readlines()
    ]


class Direction(enum.Enum):
    N = 0
    E = 1
    S = 2
    W = 3

    @property
    def vector(self) -> tuple[int, int]:
        if self == Direction.N:
            return (-1, 0)
        elif self == Direction.E:
            return (0, 1)
        elif self == Direction.S:
            return (1, 0)
        elif self == Direction.W:
            return (0, -1)
        else:
            raise ValueError(self)

    def cw(self) -> "Direction":
        if self == Direction.N:
            return Direction.E
        elif self == Direction.E:
            return Direction.S
        elif self == Direction.S:
            return Direction.W
        elif self == Direction.W:
            return Direction.N
        else:
            raise ValueError(self)

    def ccw(self) -> "Direction":
        if self == Direction.N:
            return Direction.W
        elif self == Direction.E:
            return Direction.N
        elif self == Direction.S:
            return Direction.E
        elif self == Direction.W:
            return Direction.S
        else:
            raise ValueError(self)


start_dir = Direction.E


maze = np.array(maze)
print(str_values_only(maze))
start_pos = np.where(maze == 'S')
end_pos = np.where(maze == 'E')
maze[start_pos] = '.'
maze[end_pos] = '.'
start_pos = (int(start_pos[0][0]), int(start_pos[1][0]))
end_pos = (int(end_pos[0][0]), int(end_pos[1][0]))
print(start_pos, start_dir, end_pos)


class Action(enum.Enum):
    MoveForward = 'F'
    RotateCCW = 'L'
    RotateCW = 'R'

    @property
    def points(self) -> int:
        if self == Action.MoveForward:
            return 1
        elif self.RotateCW:
            return 1000
        elif self.RotateCCW:
            return 1000
        else:
            raise ValueError(f"Unreachable {self}")


@dataclasses.dataclass
class State:
    current_pos: tuple[int, int]
    current_dir: Direction

    _history: list[Action] = dataclasses.field(default_factory=list)

    @cached_property
    def score(self) -> int:
        score = 0
        for action in self._history:
            score += action.points
        return score

    def summary(self) -> str:
        return ''.join([
            action.value
            for action in self._history
        ]) + f" ({self.current_pos} {self.current_dir.name}) => {self.score}"

    def do_action(self, action: Action) -> "State":
        if action == Action.MoveForward:
            new_pos = tuple_add(self.current_pos, self.current_dir.vector)
            new_dir = self.current_dir
        elif action == Action.RotateCW:
            new_pos = self.current_pos
            new_dir = self.current_dir.cw()
        elif action == Action.RotateCCW:
            new_pos = self.current_pos
            new_dir = self.current_dir.ccw()
        else:
            raise ValueError(f"Unreachable {action}")
        return State(
            new_pos, new_dir,
            [*self._history, action],
        )

    def options(self) -> list["State"]:
        options_ = [
            self.do_action(Action.RotateCW),
            self.do_action(Action.RotateCCW),
        ]

        forward_state = self.do_action(Action.MoveForward)
        object_in_front = maze[forward_state.current_pos]
        if object_in_front == '.':
            # we can move forward
            options_.insert(0, forward_state)
        return options_

    def visited_positions(self) -> list[tuple[int]]:
        p = self
        coords: list[tuple[int, int]] = [p.current_pos]
        for action in self._history:
            p = p.do_action(action)
            coords.append(p.current_pos)
        return coords


state = State(start_pos, start_dir)
best_score_so_far = np.full([*maze.shape, 4], None)
it = for_sendable_generator(traverse_breath_first(
    state,
    lambda s: s.options()
))
for node in it:
    #print(node.summary())
    if node.current_dir == end_pos:
        it.send(True)  # don't explore further

    node_score = node.score
    if best_score_so_far[node.current_pos][node.current_dir.value] is None:
        best_score = None
    else:
        best_score = best_score_so_far[node.current_pos][node.current_dir.value][0]
    if best_score is None or node_score < best_score.score:
        best_score_so_far[node.current_pos][node.current_dir.value] = [node]
    elif node_score == best_score.score:
        best_score_so_far[node.current_pos][node.current_dir.value].append(node)
    else:
        #print(node.summary() + "   XXX")
        it.send(True)  # don't explore further

print()
best_dir = min(best_score_so_far[end_pos], key=lambda s: s[0].score)
good_seats: set[tuple[int, int]] = set()
for path in best_dir:
    good_seats.update(path.visited_positions())

print(len(good_seats))
