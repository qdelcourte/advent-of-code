# https://adventofcode.com/2023/day/14
# --- Day 14: Parabolic Reflector Dish ---

import re
from functools import cache

TEST_INPUT = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""


@cache
def finditer(line):
    return [
        (m.start(1), m.end(1),
         DOT.sub('', m.group(1)).rjust(len(m.group(1)), '.'),  # east
         DOT.sub('', m.group(1)).ljust(len(m.group(1)), '.'))  # other
        for m in ROCKS_REGEX.finditer(line)
    ]


def part_1(lines):
    border = ['#' * len(lines[0])]
    lines = border + lines + border

    columns = list(map(''.join, zip(*lines)))

    lines_ok = {}
    for i, line in enumerate(columns):
        previous_rock = None
        for m in re.finditer(r'#', line):
            if previous_rock is None:
                previous_rock = m
            else:
                prev, curr = previous_rock.start(), m.start()
                for k in range(prev, prev + line[prev:curr].count('O')):
                    lines_ok.setdefault(k, 0)
                    lines_ok[k] += 1
                previous_rock = m

    return sum([(len(lines) - 2 - line_ok) * lines_ok[line_ok] for line_ok in lines_ok.keys()])


ROCKS_REGEX = re.compile(r'#*([O.]*O+[O.]*)#*')
DOT = re.compile(r'\.')


def part_2(data, nb_cycle):
    # 1000000000 cycles of
    # north, west, south, east
    # Compute total load of the last cycle (on the east one)

    # This function is the optimized solution of part 1
    def get_load(_lines):
        return sum([l.count('O')*(i+1) for i, l in enumerate(_lines[::-1])])

    lines = data.copy()
    find_common = {}

    for c in range(1, nb_cycle+1):
        for k in range(4):
            lines = shift(tuple(lines))

        if lines in find_common:
            # Shift rotate to the same position every (c-find_common[lines]) cycles
            # So, find the last possible cycle in order to go directly to NB_CYCLE targeted
            last_cycle = (nb_cycle - find_common[lines]) % (c-find_common[lines]) + find_common[lines]
            # Did we find it ?
            for last_lines, k in find_common.items():
                if last_cycle == k:
                    # Get load of the last cycle
                    return get_load(last_lines)
        else:
            find_common[lines] = c


def rotate(lines, reverse=False):
    if reverse:
        return list(map(''.join, zip(*lines)))[::-1]
    return list(map(''.join, zip(*lines[::-1])))


@cache
def shift(lines: tuple):
    return tuple([
        '#'.join(map(lambda g: ''.join(sorted(g)), line.split('#')))
        for i, line in enumerate(rotate(lines))
    ])


if __name__ == '__main__':
    t1 = part_1(TEST_INPUT.splitlines())
    assert t1 == 136, t1
    print(f"test 1: {t1}")
    data = open('./input.txt', 'r').read().splitlines()
    r1 = part_1(data)
    assert r1 == 106990, r1
    print(f"#1: {r1}")
    t2 = part_2(TEST_INPUT.splitlines(), nb_cycle=1000000000)
    assert t2 == 64, t2
    print(f"test 2: {t2}")
    r2 = part_2(data, nb_cycle=1000000000)
    assert r2 == 100531, r2
    print(f"#2: {r2}")
