# https://adventofcode.com/2025/day/6
# --- Day 6: Trash Compactor ---

import math
from itertools import groupby

from helpers.utils import (
	read_input_from_main
)

TEST_INPUT = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """

OPS = {"+": sum, "*": math.prod}


def part1(data):
    return sum(OPS[pb[-1]](map(int, pb[:-1])) for pb in zip(*[filter(None, line.split(' ')) for line in data]))


def part2(data):
    operators = list(filter(None, data[-1].split(' ')))
    l = [tuple(map(int, g)) for k, g in groupby(map(lambda x: ''.join(x).strip(), zip(*data[:-1])), key=bool) if k]

    return sum(OPS[operators[idx]](k) for idx, k in enumerate(l))

if __name__ == "__main__":
    test_input = TEST_INPUT.splitlines()
    r1 = part1(test_input)
    assert r1 == 4277556, r1
    data = read_input_from_main(__file__)
    r1 = part1(data)
    assert r1 == 4405895212738, r1
    print(f"#1: {r1}")
    r2 = part2(test_input)
    assert r2 == 3263827, r2
    r2 = part2(data)
    assert r2 == 7450962489289, r2
    print(f"#2: {r2}")
