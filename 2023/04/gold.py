import dataclasses


@dataclasses.dataclass
class Card:
    card_num: int
    num_have: list[int]
    num_win: list[int]

    def matches(self) -> int:
        matches = 0
        for num in self.num_have:
            if num in self.num_win:
                matches += 1
        return matches


cards: dict[int, Card] = {}
with open("input.txt", "r") as f:
    for line in f:
        line = line.rstrip()
        card, _ = line.split(': ')
        num_have, num_win = _.split(' | ')
        card = int(card[5:])
        num_have = [int(_) for _ in num_have.split()]
        num_win = [int(_) for _ in num_win.split()]
        #print(f"{card=} {num_have=} {num_win=}")
        cards[card] = Card(card_num=card, num_have=num_have, num_win=num_win)

card_copies: dict[int, int] = {_: 1 for _ in cards.keys()}
for card in cards.values():
    card_matches = card.matches()
    print(f"{card=}, {card_matches=}")
    for card_num in range(card.card_num+1, card.card_num+1 + card_matches):
        card_copies[card_num] += card_copies[card.card_num]

print(card_copies)
print(sum(card_copies.values()))
