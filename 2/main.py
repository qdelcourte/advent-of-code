# https://adventofcode.com/2023/day/2
# --- Day 2: Cube Conundrum ---

import re
from functools import reduce
from operator import mul

# 1 : only 12 red cubes, 13 green cubes, and 14 blue cubes
colors = {'red': 12, 'green': 13, 'blue': 14}
regex1 = re.compile(r'Game (\d+):(.*)')
regex2 = re.compile(r'(?P<red>\d+) red|(?P<green>\d+) green|(?P<blue>\d+) blue')


def part_1():
    result = 0
    for line in data:
        m = regex1.match(line)
        game_id = int(m.group(1))
        try:
            for s in m.group(2).split(';'):
                for m in regex2.finditer(s):
                    d = m.groupdict()
                    for c in colors.keys():
                        if d[c] and int(d[c]) > colors[c]:
                            raise Exception
        except Exception:
            continue

        result += game_id

    return result


def part_2():
    result = 0
    for line in data:
        min_sets: dict = dict(zip(colors.keys(), [None]*len(colors)))
        for s in regex1.match(line).group(2).split(';'):
            for m in regex2.finditer(s):
                d = m.groupdict()
                for c in colors.keys():
                    if d[c] and (min_sets[c] or 0) < int(d[c]):
                        min_sets[c] = int(d[c])

        result += reduce(mul, min_sets.values())

    return result


if __name__ == '__main__':
    data = open('./input.txt', 'r').readlines()
    r1 = part_1()
    assert r1 == 1931, r1
    print(f"#1: {r1}")
    r2 = part_2()
    assert r2 == 83105, r2
    print(f"#2: {r2}")
