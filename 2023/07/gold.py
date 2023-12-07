from __future__ import annotations

import dataclasses
import enum
import functools


class Card(str, enum.Enum):
    def __new__(cls, letter: str, strength: int):
        o = str.__new__(cls, letter)
        o._value_ = letter
        o.strength = strength
        return o

    Joker = ('J', 1)
    Two = ('2', 2)
    Three = ('3', 3)
    Four = ('4', 4)
    Five = ('5', 5)
    Six = ('6', 6)
    Seven = ('7', 7)
    Eight = ('8', 8)
    Nine = ('9', 9)
    Ten = ('T', 10)
    Queen = ('Q', 12)
    King = ('K', 13)
    Ace = ('A', 14)

    @classmethod
    def from_letter(cls, letter: str) -> Card:
        assert len(letter) == 1
        return cls(letter)


class HandType(enum.Enum):
    HighCard = 0
    OnePair = 1
    TwoPair = 2
    ThreeOfAKind = 3
    FullHouse = 4
    FourOfAKind = 5
    FiveOfAKind = 6


@functools.total_ordering
class Hand:
    def __init__(self, cards: list[Card]):
        assert len(cards) == 5
        self.cards = cards

    @classmethod
    def from_string(cls, string: str) -> Hand:
        return Hand([Card.from_letter(_) for _ in list(string)])

    def __repr__(self) -> str:
        return "".join([_._value_ for _ in self.cards])

    @property
    def type(self) -> HandType:
        card_count = {}
        for card in self.cards:
            card_count[card] = card_count.get(card, 0) + 1

        sorted_cards = sorted(card_count.keys(), key=lambda c: (card_count[c], c.value), reverse=True)

        if sorted_cards[0] != Card.Joker and card_count.get(Card.Joker, 0) > 0:
            # We get the strongest hand by adding the joker count to the highest count:
            card_count[sorted_cards[0]] += card_count[Card.Joker]
            card_count[Card.Joker] = 0
            sorted_cards.remove(Card.Joker)
        elif sorted_cards[0] == Card.Joker and len(sorted_cards) > 1:
            # We get the strongest hand by adding the joker count to the (second) highest count:
            card_count[sorted_cards[1]] += card_count[Card.Joker]
            card_count[Card.Joker] = 0
            sorted_cards.remove(Card.Joker)

        if card_count[sorted_cards[0]] == 5:
            return HandType.FiveOfAKind
        if card_count[sorted_cards[0]] == 4:
            return HandType.FourOfAKind
        if card_count[sorted_cards[0]] == 3 and card_count[sorted_cards[1]] == 2:
            return HandType.FullHouse
        if card_count[sorted_cards[0]] == 3:
            return HandType.ThreeOfAKind
        if card_count[sorted_cards[0]] == 2 and card_count[sorted_cards[1]] == 2:
            return HandType.TwoPair
        if card_count[sorted_cards[0]] == 2:
            return HandType.OnePair
        return HandType.HighCard

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Hand):
            return False
        return self.cards == o.cards

    def __lt__(self, o: Hand) -> bool:
        my = (self.type.value, *[_.strength for _ in self.cards])
        them = (o.type.value, *[_.strength for _ in o.cards])
        return my < them


@dataclasses.dataclass
class HandBid:
    hand: Hand
    bid: int


set_of_hands = []
with open("input.txt", "r") as f:
    for line in f:
        line = line.rstrip()
        hand, bid = line.split()
        hand_bid = HandBid(hand=Hand.from_string(hand), bid=int(bid))
        set_of_hands.append(hand_bid)


set_of_hands = sorted(set_of_hands, key=lambda hb: hb.hand)
total_winnings = 0
for i, hand_bid in enumerate(set_of_hands):
    rank = i + 1
    total_winnings += rank * hand_bid.bid

print(total_winnings)
# 251877213 too high
# 251637886 too high
# 251224870 correct
