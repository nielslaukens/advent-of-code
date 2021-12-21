import typing

with open("21.input.txt", "r") as f:
    lines = [
        line.strip()
        for line in f.readlines()
    ]


class PositionOnBoard:
    def __init__(self, pos: int):
        self._p = pos-1

    @property
    def p(self):
        return self._p + 1

    def __str__(self) -> str:
        return str(self.p)

    def __repr__(self) -> str:
        return f"PositionOnBoard({self.p})"

    def advance(self, step: int):
        self._p = (self._p + step) % 10


player_position = [
    PositionOnBoard(int(line[len("Player 1 starting position: "):]))
    for line in lines
]


class DeterministicDie:
    def __init__(self):
        self._state = 0
        self.sides = 100
        self.rolls = 0

    def roll(self) -> int:
        self.rolls += 1
        side = self._state + 1
        self._state = (self._state + 1) % self.sides
        return side


class Win(Exception):
    pass


class Game:
    def __init__(self, positions: typing.List[PositionOnBoard], die: DeterministicDie):
        self.positions = positions
        self.scores = [
            0
            for _ in positions
        ]
        self.die = die
        self.next_player = 0

    def play_one_turn(self):
        # roll 3 times
        advance = self.die.roll() + self.die.roll() + self.die.roll()
        self.positions[self.next_player].advance(advance)
        self.scores[self.next_player] += self.positions[self.next_player].p
        if self.scores[self.next_player] >= 1000:
            raise Win(self.next_player)
        self.next_player = (self.next_player + 1) % len(self.positions)

    def __repr__(self) -> str:
        return f"Game(pos={self.positions}, score={self.scores}, next={self.next_player})"

game = Game(player_position, DeterministicDie())
print(game)
try:
    for turn in range(1000):
        game.play_one_turn()
        print(game)
except Win:
    print(f"Player {game.next_player} won with {game.scores[game.next_player]} points.")
    assert len(player_position) == 2
    print(f"Other player {1-game.next_player} has {game.scores[1-game.next_player]} points")
    print(game)
    print(f"Die rolled {game.die.rolls} times")
    print(f"Puzzle output: {game.scores[1-game.next_player] * game.die.rolls}")
