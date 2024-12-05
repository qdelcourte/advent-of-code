# https://adventofcode.com/2023/day/12
# --- Day 13: Point of Incidence ---

from itertools import groupby


TEST_INPUT = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""


def split_list(lst, val):
    return [list(group) for k,
            group in groupby(lst, lambda x: x == val) if not k]


def get_differences(list1, list2):
    return [
        index
        for index, (first, second) in enumerate(zip(list1, list2))
        if first != second
    ]


def find_reflection(lst, allowed_diff=0):
    for i, line in enumerate(lst, start=1):
        m = min(i, len(lst) - i)
        left = lst[i - m: i]
        right = lst[i: i + m]
        right_reversed = list(reversed(right))
        if left and right and len(get_differences(''.join(left), ''.join(right_reversed))) == allowed_diff:
            return i


def solve(mirrors, allowed_diff):
    result = 0
    for k, mirror in enumerate(mirrors):
        # Check horizontal
        if i := find_reflection(mirror, allowed_diff):
            result += 100 * i

        # Check vertical
        columns = [
            ''.join([line[i] for line in mirror])
            for i in range(0, len(mirror[0]))
        ]

        if i := find_reflection(columns, allowed_diff):
            result += i

    return result


def test_1():
    return solve(split_list(TEST_INPUT.splitlines(), ''), allowed_diff=0)


def part_1():
    return solve(split_list(data, ''), allowed_diff=0)


def test_2():
    return solve(split_list(TEST_INPUT.splitlines(), ''), allowed_diff=1)


def part_2():
    return solve(split_list(data, ''), allowed_diff=1)


if __name__ == '__main__':
    t1 = test_1()
    assert t1 == 405, t1
    print(f"test 1: {t1}")
    data = open('./input.txt', 'r').read().splitlines()
    r1 = part_1()
    assert r1 == 35691, r1
    print(f"#1: {r1}")
    t2 = test_2()
    assert t2 == 400, t2
    print(f"test 2: {t2}")
    r2 = part_2()
    assert r2 == 39037, r2
    print(f"#2: {r2}")
