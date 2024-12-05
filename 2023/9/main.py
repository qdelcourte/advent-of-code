# https://adventofcode.com/2023/day/9
# --- Day 9: Mirage Maintenance ---

from functools import reduce


def solve(reverse=False):
    def differences(sequence):
        return [x - sequence[i - 1] for i, x in enumerate(sequence)][1:]

    def get_next(sequence):
        result = sequence[-1]
        while any(sequence):
            sequence = differences(sequence)
            result += sequence[-1]
        return result

    return reduce(lambda acc, seq: acc + get_next(list(map(int, reversed(seq) if reverse else seq))),
                  map(str.split, lines), 0)


def part_1():
    return solve()


def part_2():
    return solve(reverse=True)


if __name__ == '__main__':
    lines = open('./input.txt', 'r').read().splitlines()
    r1 = part_1()
    assert r1 == 1987402313, r1
    print(f"#1: {r1}")
    r2 = part_2()
    assert r2 == 900, r2
    print(f"#2: {r2}")
