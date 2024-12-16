import enum
import typing

import numpy as np

from tools.numpy_tools import str_values_only


class Direction(enum.Enum):
    Up = '^'
    Right = '>'
    Down = 'v'
    Left = '<'

    def coord(self) -> tuple[int, int]:
        if self == Direction.Up:
            return (-1, 0)
        elif self == Direction.Right:
            return (0, 1)
        elif self == Direction.Down:
            return (1, 0)
        elif self == Direction.Left:
            return (0, -1)
        else:
            raise ValueError(f"unknown value {self}")


NTuple = typing.TypeVar('NTuple', bound=tuple[int, ...])
def add(a: NTuple, b: NTuple) -> NTuple:
    if len(a) != len(b):
        raise ValueError(f"Different number of dimensions: {len(a)} != {len(b)}")
    return tuple(
        a[d] + b[d]
        for d in range(len(a))
    )


warehouse = []
movement_attempts: list[Direction] = []
state = 'warehouse'
with open("input.txt", "r") as f:
    for line in f:
        line = line.strip()
        if line == "":
            state = 'movement'
            continue
        if state == 'warehouse':
            warehouse.append(list(line))
        elif state == 'movement':
            movement_attempts.extend(
                Direction(char)
                for char in list(line)
            )
        else:
            raise RuntimeError(f'Unexpected state {state}')

warehouse = np.array(warehouse)
robot = np.where(warehouse == '@')
robot = (int(robot[0][0]), int(robot[1][0]))
print(str_values_only(warehouse))
print(robot)
print(movement_attempts)


class Wall(Exception):
    pass


def push(pos: tuple[int, int], direction: Direction, char: str = 'O') -> tuple[int, int]:
    new_pos = add(pos, direction.coord())
    if warehouse[new_pos] == '.':
        pass
    elif warehouse[new_pos] == '#':
        raise Wall()
    elif warehouse[new_pos] == 'O':
        push(new_pos, movement_attempt)
    warehouse[pos] = '.'
    warehouse[new_pos] = char
    return new_pos


for movement_attempt in movement_attempts:
    try:
        robot = push(robot, movement_attempt, '@')
    except Wall:
        pass
    #print()
    #print(movement_attempt)
    #print(str_values_only(warehouse))

boxes = np.array(np.where(warehouse == 'O')).transpose()
sum_gps = 0
for box in boxes:
    gps = 100*box[0] + box[1]
    print(box, gps)
    sum_gps += gps

print(sum_gps)
