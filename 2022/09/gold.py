from __future__ import annotations

import enum
import dataclasses

import numpy as np


class Direction(enum.Enum):
    def __new__(cls, letter: str, vector: np.ndarray) -> Direction:
        obj = object.__new__(cls)
        obj._value_ = letter
        obj.vector = vector
        return obj

    Right = ('R', np.array([1, 0]))
    Left = ('L', np.array([-1, 0]))
    Up = ('U', np.array([0, 1]))
    Down = ('D', np.array([0, -1]))


@dataclasses.dataclass
class Move:
    direction: Direction
    amount: int


moves = []
with open("input.txt", "r") as f:
    for line in f:
        line = line.rstrip()
        direction, amount = line.split()
        direction = Direction(direction)
        amount = int(amount)
        moves.append(Move(direction, amount))


def update_tail(head_pos: np.ndarray, tail_pos: np.ndarray) -> np.ndarray:
    dx = head_pos[0] - tail_pos[0]
    dy = head_pos[1] - tail_pos[1]
    if abs(dx) <= 1 and abs(dy) <= 1:
        return tail_pos
    elif dx == 0 and abs(dy) >= 2:
        return np.array([tail_pos[0], tail_pos[1] + dy/2])
    elif dy == 0 and abs(dx) >= 2:
        return np.array([tail_pos[0] + dx/2, tail_pos[1]])
    elif dx != 0 and dy != 0:
        return np.array([tail_pos[0] + (1 if dx > 0 else -1),
                         tail_pos[1] + (1 if dy > 0 else -1),
                         ])
    else:
        raise ValueError(f"tail {tail_pos} in strange position of head {head_pos}")

rope_pos = np.zeros(shape=(10, 2))  # x (horizontal, increases to the right), y (vertical, increases to the top)
tail_positions = set()
for move in moves:
    for step in range(move.amount):
        rope_pos[0, :] = rope_pos[0, :] + move.direction.vector
        for k in range(1, rope_pos.shape[0]):
            rope_pos[k, :] = update_tail(rope_pos[k - 1, :], rope_pos[k])
        print(rope_pos)
        tail_positions.add((rope_pos[9, 0], rope_pos[9, 1]))

print(len(tail_positions))
