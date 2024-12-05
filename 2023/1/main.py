# https://adventofcode.com/2023/day/1
# --- Day 1: Trebuchet?! ---

import re
from functools import reduce


def part_1():
    return reduce(
        lambda acc, line: acc + int(line[0] + line[-1]),
        map(lambda line: re.sub(r'[a-z]+', '', line), data), 0
    )


def part_2():
    figures = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    rep = lambda v: str(figures.index(v)+1) if v in figures else v # noqa

    return reduce(
        lambda acc, x: acc + int(x[0] + x[-1]),
        map(lambda line:
            list(
                map(rep, re.findall(rf"(?=(\d|{'|'.join(figures)}))", line))
            ), data), 0
    )


if __name__ == '__main__':
    data = open('./input.txt', 'r').read().splitlines()
    r1 = part_1()
    assert r1 == 56506, r1
    print(f"#1: {r1}")
    r2 = part_2()
    assert r2 == 56017, r2
    print(f"#2: {r2}")
