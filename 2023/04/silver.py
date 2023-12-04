import dataclasses


@dataclasses.dataclass
class Card:
    card_num: int
    num_have: list[int]
    num_win: list[int]

cards: list[Card] = []
with open("input.txt", "r") as f:
    for line in f:
        line = line.rstrip()
        card, _ = line.split(': ')
        num_have, num_win = _.split(' | ')
        card = int(card[5:])
        num_have = [int(_) for _ in num_have.split()]
        num_win = [int(_) for _ in num_win.split()]
        #print(f"{card=} {num_have=} {num_win=}")
        cards.append(Card(card_num=card, num_have=num_have, num_win=num_win))

total_worth = 0
for card in cards:
    card_worth = 0
    for num in card.num_have:
        if num in card.num_win:
            if card_worth == 0:
                card_worth = 1
            else:
                card_worth *= 2

    total_worth += card_worth
    print(f"{card=}, {card_worth=}")

print(total_worth)
