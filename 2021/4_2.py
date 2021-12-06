import sys
import typing


class Bingo(Exception):
    def __init__(self, msg, score):
        super().__init__(msg)
        self.score = score


class BingoBoard:
    def __init__(self, board: typing.List[typing.List[int]], name: str = ""):
        self.name = name
        self.board = board
        self.marked = [
            [False for col in range(0, len(board[0]))]
            for row in range(0, len(board))
        ]
        self.done = False

    def mark(self, num: int):
        if self.done:
            return

        for i, row in enumerate(self.board):
            for j, col in enumerate(row):
                if col == num:
                    self.marked[i][j] = True
        if self.check_bingo():
            self.done = True
            raise Bingo(f"bingo", self.score() * num)

    def check_bingo(self) -> bool:
        # check rows
        for i, row in enumerate(self.marked):
            all_true = True
            for col in row:
                all_true = all_true and col
            if all_true:
                print(f"BINGO Board {self.name}, row {i}")
                return True

        # check columns
        for j in range(0, len(self.marked[0])):
            all_true = True
            for i in range(0, len(self.marked)):
                all_true = all_true and self.marked[i][j]
            if all_true:
                print(f"BINGO Board {self.name}, column {j}")
                return True

        return False

    def score(self) -> int:
        s = 0
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board[0])):
                if not self.marked[i][j]:
                    s += self.board[i][j]
        return s


boards = []
with open("4_1.input.txt", "r") as f:
    draw_numbers = [int(num) for num in f.readline().rstrip().split(',')]
    b = 1
    while True:
        empty_line = f.readline()
        if empty_line == "":
            break
        boards.append(BingoBoard([
            [int(col) for col in f.readline().strip().split()]
            for row in range(0, 5)
        ], str(b)))
        b = b + 1

last_board_to_win = None
boards_in_game = len(boards)
for draw in draw_numbers:
    print(f"Draw {draw}")
    for board in boards:
        try:
            board.mark(draw)
        except Bingo as e:
            boards_in_game -= 1
            if boards_in_game == 0:
                print(f"Last board to win: {board.name}")
                print(f"Score: {e.score}")
                sys.exit(0)
