import itertools

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


example = Prng(123)
example_expected = [15887950, 16495136, 527345, 704524, 1553684, 12683156, 11100544, 12249484, 7753432, 5908254]
assert [next(example) for _ in range(len(example_expected))] == example_expected


def price_list(start_secret: int, items: int = 2001) -> list[int]:
    monkey = Prng(start_secret)
    out = [start_secret % 10]
    for _ in range(items-1):
        out.append(next(monkey) % 10)
    return out


assert price_list(123, 10) == [3, 0, 6, 5, 4, 4, 6, 4, 4, 2]


def delta_list(price_list: list[int]) -> list[int]:
    out = []
    for a, b in itertools.pairwise(price_list):
        out.append(b-a)
    return out


assert delta_list(price_list(123, 10)) == [-3, 6, -1, -1, 0, 2, -2, 0, -2]

buyer_price_list = []
buyer_delta_list = []
with open("input.txt", "r") as f:
    for line in f:
        line = int(line)
        pl = price_list(line)
        buyer_price_list.append(pl)
        buyer_delta_list.append(delta_list(pl))


def sell_with_instruction(seq: list[int]) -> list[int | None]:
    buyer_price = []
    for buyer, delta_list in enumerate(buyer_delta_list):
        for end_idx in range(len(seq), len(delta_list)):
            buyer_delta = delta_list[end_idx-len(seq):end_idx]
            if buyer_delta != seq:
                continue
            price = buyer_price_list[buyer][end_idx]
            buyer_price.append(price)
            break  # go to next buyer
        else:
            buyer_price.append(None)
    return buyer_price


buyer_price_for_sequence: list[dict[tuple[int, int, int, int], int]] = [
    {}
    for buyer in range(len(buyer_price_list))
]
all_seen_sequences: set[tuple[int, int, int, int]] = set()
for buyer in range(len(buyer_price_list)):
    #print(f"Mapping sequence to price for buyer {buyer}")
    for end_idx in range(4, len(buyer_delta_list[buyer])+1):
        seq = tuple(buyer_delta_list[buyer][end_idx-4:end_idx])
        if seq in buyer_price_for_sequence[buyer]:
            # this sequence is already seen; so the monkey would have already taken *that* opportunity
            pass
        else:
            # first time this sequence appears
            buyer_price_for_sequence[buyer][seq] = buyer_price_list[buyer][end_idx]
            all_seen_sequences.add(seq)

print(f"{len(all_seen_sequences)} sequences seen")
best_seq = None
best_price = 0
for seq in all_seen_sequences:
    price_of_seq = 0
    for buyer in range(len(buyer_price_list)):
        price_of_seq += buyer_price_for_sequence[buyer].get(seq, 0)
    if price_of_seq > best_price:
        print(f"{seq} yields {price_of_seq}")
        #assert price_of_seq == sum(_ for _ in sell_with_instruction(list(seq)) if _ is not None)
        best_price = price_of_seq
        best_seq = seq

print(f"Best sequence: {best_seq} yields {best_price}")
