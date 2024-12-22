class Prng:
    def __init__(self, secret: int):
        self.secret = secret

    def __next__(self) -> int:
        step1 = self.secret * 64
        self.secret = (self.secret ^ step1) % 16777216

        step2 = self.secret // 32
        self.secret = (self.secret ^ step2) % 16777216

        step3 = self.secret * 2048
        self.secret = (self.secret ^ step3) % 16777216

        return self.secret


example1 = Prng(123)
example1_expected = [15887950, 16495136, 527345, 704524, 1553684, 12683156, 11100544, 12249484, 7753432, 5908254]
assert [next(example1) for _ in range(len(example1_expected))] == example1_expected

total_secret = 0
with open("input.txt", "r") as f:
    for line in f:
        line = int(line)
        buyer = Prng(line)
        #buyers.append(buyer)
        for i in range(2000):
            next(buyer)
        print(f"{line}: {buyer.secret}")
        total_secret += buyer.secret

print(total_secret)
