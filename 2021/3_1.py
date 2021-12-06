class BitCount:
    def __init__(self):
        self.count_false = 0
        self.count_true = 0

    def add(self, bit: bool):
        if bit:
            self.add_true()
        else:
            self.add_false()

    def add_true(self):
        self.count_true += 1

    def add_false(self):
        self.count_false += 1

    def most_common(self):
        if self.count_true > self.count_false:
            return True
        elif self.count_false > self.count_true:
            return False
        else:
            raise ValueError("Both equally common")

bit_counts = None
with open("3_1.input.txt", "r") as f:
    for line in f.readlines():
        bits = list(line.rstrip())
        if bit_counts is None:
            bit_counts = [
                BitCount()
                for _ in range(0, len(bits))
            ]
        for i, bit in enumerate(bits):
            bit_counts[i].add(bit == '1')

gamma_rate = [
    bit_count.most_common()
    for bit_count in bit_counts
]
epsilon_rate = [
    not _
    for _ in gamma_rate
]

gamma_rate = ''.join(['1' if _ else '0' for _ in gamma_rate])
epsilon_rate = ''.join(['1' if _ else '0' for _ in epsilon_rate])
gamma_rate = int(gamma_rate, 2)
epsilon_rate = int(epsilon_rate, 2)

print(f"gamma rate = {gamma_rate}")
print(f"epsilon rate = {epsilon_rate}")
print(f"Product = {gamma_rate * epsilon_rate}")
