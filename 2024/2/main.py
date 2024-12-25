# https://adventofcode.com/2024/day/2
# --- Day 2: Red-Nosed Reports ---

TEST_INPUT = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""


def part_1(lines):
    return sum(int(check(list(map(int, line.split())))) for line in lines)


def check(levels):
    return all(0 < abs(levels[i - 1] - level) <= 3 and
               (i == 1 or (levels[i - 1] - level > 0) == (levels[0] - levels[1] > 0))
               for i, level in enumerate(levels[1:], 1))


def part_2(lines):
    return sum(
        check(levels := list(map(int, line.split()))) or
        any(check(levels[:i] + levels[i+1:]) for i in range(len(levels)))
        for line in lines
    )


if __name__ == '__main__':
    test_input = TEST_INPUT.splitlines()
    r1 = part_1(test_input)
    assert r1 == 2, r1
    data = open('./input.txt', 'r').read().splitlines()
    r1 = part_1(data)
    assert r1 == 524, r1
    r2 = part_2(test_input)
    assert r2 == 4, r2
    r2 = part_2(data)
    assert r2 == 569, r2
