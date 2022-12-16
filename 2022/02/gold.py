import enum
import typing


class RPS(enum.Enum):
    Rock = 1
    Paper = 2
    Scissor = 3


class Outcome(enum.Enum):
    Loss = 'X'
    Draw = 'Y'
    Win = 'Z'


def rps(my: RPS, opponent: RPS) -> typing.Tuple[Outcome, int]:
    if my == opponent:
        return Outcome.Draw, my.value + 3

    if my.value == (opponent.value % 3) + 1:
        # Rock -> Paper, Paper -> Scissor, Scissor -> Rock
        return Outcome.Win, my.value + 6

    return Outcome.Loss, my.value + 0


total_score = 0

with open("input.txt", "r") as f:
    for line in f:
        line = line.rstrip().split()
        opponent = RPS(ord(line[0]) - ord('A') + 1)
        desired_outcome = Outcome(line[1])
        if desired_outcome == Outcome.Draw:
            my = opponent
        elif desired_outcome == Outcome.Win:
            my = RPS((opponent.value % 3) + 1)
        elif desired_outcome == Outcome.Loss:
            my = RPS((opponent.value - 2) % 3 + 1)
        else:
            raise ValueError(desired_outcome)

        score = rps(my, opponent)
        assert score[0] == desired_outcome
        total_score += score[1]

print(total_score)
