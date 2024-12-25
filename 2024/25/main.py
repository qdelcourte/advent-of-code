# https://adventofcode.com/2024/day/25
# --- Day 25: Code Chronicle ---

import numpy as np

TEST_INPUT = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""


def parse(lines):
    locks, keys, curr = [], [], None
    for line in lines + ['']:
        if curr is None and line == '#####':
            curr = [0] * 5, 'lock'
        elif curr is None and line == '.....':
            curr = [-1] * 5, 'key'
        elif line == '':
            curr = (locks if curr[1] == 'lock' else keys).append(curr[0])
        elif curr:
            for i, ch in enumerate(line):
                if ch == '#':
                    curr[0][i] += 1

    return locks, keys


def part_1(lines):
    locks, keys = parse(lines)
    return sum(
        not any(x > 5 for x in np.add(lock, key))
        for lock in locks
        for key in keys)


if __name__ == '__main__':
    test_input = TEST_INPUT.splitlines()
    r1 = part_1(test_input)
    assert r1 == 3, r1
    data = open('./input.txt', 'r').read().splitlines()
    r1 = part_1(data)
    assert r1 == 3114, r1
