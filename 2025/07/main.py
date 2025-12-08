# https://adventofcode.com/2025/day/7
# --- Day 7: Laboratories ---

from helpers.utils import (
    read_input_from_main, str_to_matrix
)

TEST_INPUT = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""

def solve(data):
    m = str_to_matrix(data, type=str)

    timelines = [0] * len(data[0])
    timelines[data[0].index('S')] = 1
    splits = 0
    for line in m[1:]:
        for x, c in enumerate(line):
            if c == '^' and timelines[x] != 0:
                splits += 1
                timelines[x - 1] += timelines[x]
                timelines[x + 1] += timelines[x]
                timelines[x] = 0

    return splits, sum(timelines)

def part1(data):
    return solve(data)[0]

def part2(data):
    return solve(data)[1]

if __name__ == "__main__":
    test_input = TEST_INPUT.splitlines()
    r1 = part1(test_input)
    assert r1 == 21, r1
    data = read_input_from_main(__file__)
    r1 = part1(data)
    assert r1 == 1541, r1
    print(f"#1: {r1}")
    r2 = part2(test_input)
    assert r2 == 40, r2
    r2 = part2(data)
    assert r2 == 80158285728929, r2
    print(f"#2: {r2}")
