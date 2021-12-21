import itertools
import typing

import numpy


with open("21.input.txt", "r") as f:
    lines = [
        line.strip()
        for line in f.readlines()
    ]

player_position = [
    int(line[len("Player 1 starting position: "):])
    for line in lines
]
assert len(player_position) == 2

three_dirac_rolls_result = {}  # What roll result occurs how many times
for d1, d2, d3 in itertools.product({1, 2, 3}, {1, 2, 3}, {1, 2, 3}):
    s = d1 + d2 + d3
    three_dirac_rolls_result[s] = three_dirac_rolls_result.get(s, 0) + 1


# We keep the game-state in a multidimensional array
# counting how many of the parallel universes are in this state
# The game state is completely defined by
#  - position of both players
#  - score of both players
#  - who's turn it is
#
# We can put an upper bound on the score.
# Since the dice will result in 3-9 steps advancement, you can't land
# on the same spot twice.
# Worst possible outcomes is:
# @2, throw 9 => 1  (1)
# @1, throw 3 => 4  (5)
# @4, throw 9 => 3  (8)
# @3, throw 9 => 2  (10)
# @2, throw 9 => 1  (11)
# @1, throw 3 => 4  (15)
# @4, throw 9 => 3  (18)
# @3, throw 9 => 2  (20)
# @2, throw 9 => 1  (21, win)
# => we will always finish it at most 9 turns
#
# We can skip the "who's turn it is" by playing a round at a time.
# After each round, the result will be either a win for player 1,
# a win for player 2, or inconclusive
#
# game_state[player_1_position][player_2_position][player_1_score][player_2_score] = occurrences
game_state = numpy.zeros((10, 10, 21+1, 21+1), dtype=int)
game_state[player_position[1-1]-1, player_position[2-1]-1, 0, 0] = 1


def shift_and_accumulate(a: numpy.ndarray, num, axis, fill=0):
    # Make our life easier and rollaxis so we shift along axis 0 (undo at the end)
    a = numpy.rollaxis(a, axis=axis)

    fill_shape = list(a.shape)
    fill_shape[0] = num

    axis_len = a.shape[0]

    out = numpy.concatenate([
        numpy.ones(fill_shape) * fill,
        a[0:(axis_len-num-1), ...],
        numpy.expand_dims(numpy.sum(a[(axis_len-num-1):, ...], axis=0), axis=0),
    ])

    out = numpy.rollaxis(out, axis=0, start=axis+1)
    return out


def do_turn(state, player: int):
    if player == 1:
        # rollaxis so we always do player1 (index 0)
        state = numpy.rollaxis(state, 1, 0)  # roll player axis to front => p2, p1, s1, s2
        state = numpy.rollaxis(state, 3, 2)

    new_state = numpy.zeros(state.shape, dtype=int)
    for possible_roll, occurrences in three_dirac_rolls_result.items():
        advanced_game_state = numpy.roll(state, possible_roll, axis=0)
        for new_pos0 in range(0, 10):
            new_pos1 = new_pos0 + 1
            advanced_game_state[new_pos0, :, :, :] = shift_and_accumulate(
                advanced_game_state[new_pos0:(new_pos0+1), :, :, :],  # use slice for 1st axis to keep dimension
                new_pos1,  # shift score up by new position (1-based)
                axis=2,
            )
        new_state += advanced_game_state * occurrences

    if player == 1:
        # roll back
        new_state = numpy.rollaxis(new_state, 0, 1+1)
        new_state = numpy.rollaxis(new_state, 2, 3+1)
    return new_state


wins = [0, 0]
for turn in range(9+1):
    game_state = do_turn(game_state, 0)
    num_wins = numpy.sum(game_state[:, :, 21, :])
    if num_wins:
        wins[0] += num_wins
        game_state[:, :, 21, :] = 0  # remove these winning universes from further consideration

    game_state = do_turn(game_state, 1)
    num_wins = numpy.sum(game_state[:, :, :, 21])
    if num_wins:
        wins[1] += num_wins
        game_state[:, :, :, 21] = 0  # remove these winning universes from further consideration

assert numpy.max(game_state) == 0
print(wins)
print(max(wins))
