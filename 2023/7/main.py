# https://adventofcode.com/2023/day/7
# --- Day 7: Camel Cards ---

from collections import Counter
from functools import reduce


"""
Five of a kind, where all five cards have the same label: AAAAA
Four of a kind, where four cards have the same label and one card has a different label: AA8AA
Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
High card, where all cards' labels are distinct: 23456
"""
PATTERNS = [[5], [1, 4], [2, 3], [1, 1, 3], [1, 2, 2], [1, 1, 1, 2], [1, 1, 1, 1, 1]]


def solve(cast: callable = lambda x: "0123456789TJQKA".index(x), transform: callable = lambda x: x):
    hands_pattern = {
        hand: (PATTERNS.index(sorted(Counter(transform(hand)).values())), list(map(cast, hand)), int(bid))
        for hand, bid in map(str.split, data)
    }

    sorted_hands = dict(sorted(hands_pattern.items(), key=lambda x: (-x[1][0], x[1][1])))
    return reduce(lambda acc, x: acc + (hands_pattern[x[1]][2] * (x[0] + 1)), enumerate(sorted_hands.keys()), 0)


def part_1():
    return solve()


def part_2():
    cast = lambda x: "J123456789TQKA".index(x)

    def best_hand(hand):
        if 'J' not in hand or 'J' * len(hand) == hand:
            return hand

        # Cards frequencies except 'J'
        c = Counter(list(hand.replace('J', '')))
        # Find the biggest most common card
        best_card = sorted(c.most_common(), key=lambda x: (x[1], cast(x[0])), reverse=True)[0][0]
        # Replace all 'J' by this card
        return hand.replace('J', best_card)

    return solve(cast, best_hand)


if __name__ == '__main__':
    data = open('./input.txt', 'r').read().splitlines()
    r1 = part_1()
    assert r1 == 255048101, r1
    print(f"#1: {r1}")
    r2 = part_2()
    assert r2 == 253718286, r2
    print(f"#2: {r2}")
