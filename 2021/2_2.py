class Submarine:
    def __init__(self):
        self.depth = 0
        self.pos = 0
        self.aim = 0

    def forward(self, n: int):
        self.pos += n
        self.depth += self.aim * n

    def up(self, n: int):
        self.aim -= n

    def down(self, n: int):
        self.aim += n


sub = Submarine()
with open("2_1.input.txt", "r") as f:
    for line in f.readlines():
        line = line.rstrip()
        action, amount = line.split()
        if action == "forward":
            sub.forward(int(amount))
        elif action == "up":
            sub.up(int(amount))
        elif action == "down":
            sub.down(int(amount))
        else:
            raise ValueError(f"Unrecognized action `{action}`")

print(f"Sub at {sub.pos}h, {sub.depth} deep")
print(f"Product: {sub.pos * sub.depth}")
