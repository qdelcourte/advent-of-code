# https://adventofcode.com/2025/day/4
# --- Day 4: Printing Department ---

from helpers.utils import (
    read_input_from_main, str_to_matrix
)

TEST_INPUT = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""

def get_nb_rolls_candidates(m, i, j):
    c = 0
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
        ni, nj = i + di, j + dj
        if 0 <= ni < len(m) and 0 <= nj < len(m[0]):
            if m[ni][nj] == '@':
                c += 1
    return c

def part1(data):
    m = str_to_matrix(data, type=str)

    return sum(
        1
        for i, row in enumerate(m)
        for j, ch in enumerate(row)
        if ch == '@' and get_nb_rolls_candidates(m, i, j) < 4
    )


def part2(data):
    m = str_to_matrix(data, type=str)
    r = 0

    can_access = True
    while can_access:
        can_access = False
        rolls_to_remove = set()

        for i, row in enumerate(m):
            for j, ch in enumerate(row):
                if ch == '@' and get_nb_rolls_candidates(m, i, j) < 4:
                    r += 1
                    rolls_to_remove.add((i, j))
                    can_access = True

        for ri, rj in rolls_to_remove:
            m[ri][rj] = '.'

    return r

if __name__ == "__main__":
    test_input = TEST_INPUT.splitlines()
    r1 = part1(test_input)
    assert r1 == 13, r1
    data = read_input_from_main(__file__)
    r1 = part1(data)
    assert r1 == 1578, r1
    print(f"#1: {r1}")
    r2 = part2(test_input)
    assert r2 == 43, r2
    r2 = part2(data)
    assert r2 == 10132, r2
    print(f"#2: {r2}")
