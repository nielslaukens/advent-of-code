import itertools

import numpy as np

from tools import numpy_tools

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
blocks_iter = itertools.cycle(blocks)
jet_iter = itertools.cycle(jet_directions)

chamber = np.empty(shape=(0, 7), dtype="<U1")
def print_chamber(ch):
    # Chamber is indexed (y, x)
    # x measures to the right
    # y measures to the top => flip axis 0 and print
    flipped = np.flip(ch, axis=0)
    print(numpy_tools.str_values_only(flipped))
    print("#" * ch.shape[1])
    print()


def top_of_stack() -> int:
    if chamber.shape[0] == 0:
        return 0

    for y in range(chamber.shape[0]):
        if np.all(chamber[y, :] == '.'):
            break
    else:
        y = chamber.shape[0]

    return y


def extend_chamber(top: int) -> None:
    global chamber
    if top <= chamber.shape[0]:
        return
    chamber = np.vstack([
        chamber,
        np.full(shape=(top - chamber.shape[0], chamber.shape[1]), fill_value='.')
    ])


class Collision(Exception):
    pass


def try_move(
        rock: np.ndarray,
        rock_lb_pos: tuple[int, int],
        move: tuple[int, int],
        ignore_if_collide: bool,
) -> tuple[int, int]:
    try:
        return _try_move(rock, rock_lb_pos, move)
    except Collision:
        if ignore_if_collide:
            return rock_lb_pos
        else:
            raise

def _try_move(
        rock: np.ndarray,
        rock_lb_pos: tuple[int, int],
        move: tuple[int, int],
) -> tuple[int, int]:
    new_pos = (rock_lb_pos[0] + move[0], rock_lb_pos[1] + move[1])
    if new_pos[0] < 0:
        raise Collision()  # with ground
    if new_pos[1] < 0:
        raise Collision()  # with left wall (right wall will raise during overlay())
    try:
        _ = overlay(rock, new_pos)  # may raise
    except (Collision, IndexError):
        raise Collision()
    return new_pos


def overlay(rock: np.ndarray, rock_lb_pos: tuple[int, int], symbol: str = '@') -> np.ndarray:
    ch = np.copy(chamber)
    it = np.nditer(rock, flags=['multi_index'])
    for block_or_empty in it:
        y, x = it.multi_index
        if block_or_empty == 1:
            if ch[(y + rock_lb_pos[0]), (x + rock_lb_pos[1])] != '.':
                raise Collision()
            ch[(y + rock_lb_pos[0]), (x + rock_lb_pos[1])] = symbol
    return ch


for rock_num in range(2022):
    falling_rock = next(blocks_iter)
    rock_lb_pos = (top_of_stack() + 3, 2)  # (y, x)
    extend_chamber(rock_lb_pos[0] + falling_rock.shape[0])
    _ = overlay(falling_rock, rock_lb_pos)  # assert no collisions
    # print_chamber(_)

    try:
        while True:  # until exception
            # jet:
            jet_direction = next(jet_iter)
            if jet_direction == '>':
                rock_lb_pos = try_move(falling_rock, rock_lb_pos, (0, 1), ignore_if_collide=True)
            else:  # <, move left
                rock_lb_pos = try_move(falling_rock, rock_lb_pos, (0, -1), ignore_if_collide=True)
            # print(f"after jet {jet_direction}: {rock_lb_pos}")
            # print_chamber(overlay(falling_rock, rock_lb_pos))

            # drop:
            rock_lb_pos = try_move(falling_rock, rock_lb_pos, (-1, 0), ignore_if_collide=False)  # may raise
            # print(f"after drop: {rock_lb_pos}")
            # print_chamber(overlay(falling_rock, rock_lb_pos))
    except Collision:
        chamber = overlay(falling_rock, rock_lb_pos, '#')
        print(f"After {rock_num+1} rocks:")
        # print_chamber(chamber)

print(top_of_stack())
