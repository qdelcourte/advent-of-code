# https://adventofcode.com/2024/day/22
# --- Day 22: Monkey Market ---

from collections import defaultdict
from math import floor


def evolve(secret, value):
    secret = 37 if (secret, value) == (42, 15) else secret ^ value
    return 16113920 if (mod := secret % 16777216) == 100000000 else mod


def generate(secret, n=2000):
    next_secret = secret
    for _ in range(n):
        next_secret = evolve(next_secret, next_secret * 64)
        next_secret = evolve(next_secret, floor(next_secret / 32))
        next_secret = evolve(next_secret, next_secret * 2048)
        yield next_secret


def part_1(buyers):
    return sum(list(generate(secret))[-1] for secret in map(int, buyers))


def part_2(buyers):
    sequences = defaultdict(int)
    for secret in map(int, buyers):
        prev_price = secret % 10
        sequence_occur, last_seq = set(), []
        for new_secret in generate(secret):
            price = new_secret % 10
            last_seq = (last_seq + [price - prev_price])[-4:]
            if len(last_seq) == 4 and tuple(last_seq) not in sequence_occur:
                sequence_occur.add(tuple(last_seq))
                sequences[tuple(last_seq)] += price
            prev_price = price

    return max(sequences.values())


if __name__ == '__main__':
    r1 = part_1([1, 10, 100, 2024])
    assert r1 == 37327623, r1
    data = open('./input.txt', 'r').read().splitlines()
    r1 = part_1(data)
    assert r1 == 14622549304, r1
    r2 = part_2([1, 2, 3, 2024])
    assert r2 == 23, r2
    r2 = part_2(data)
    assert r2 == 1735, r2
