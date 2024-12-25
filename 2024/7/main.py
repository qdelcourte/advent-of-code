# https://adventofcode.com/2024/day/7
# --- Day 7: Bridge Repair ---

from operator import mul, add


TEST_INPUT = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""


def dfs(operators, test_value, curr, rest, i):
    if curr > test_value or i == len(rest):
        if test_value == curr:
            return test_value
        return None

    for op in operators:
        if dfs(operators, test_value, op(curr, rest[i]), rest, i+1):
            return test_value


def compute(lines, operators):
    r = 0
    for line in lines:
        line_split = line.split()
        test_value = int(line_split[0][:-1])
        eq_values = list(map(int, line_split[1:]))
        r += dfs(operators, test_value, eq_values[0], eq_values, 1) or 0
    return r


def part_1(lines):
    return compute(lines, [add, mul])


def part_2(lines):
    return compute(lines, [add, mul, lambda a, b: int(f"{a}{b}")])


if __name__ == '__main__':
    test_input = TEST_INPUT.splitlines()
    r1 = part_1(test_input)
    assert r1 == 3749, r1
    data = open('./input.txt', 'r').read().splitlines()
    r1 = part_1(data)
    assert r1 == 4998764814652, r1
    r2 = part_2(test_input)
    assert r2 == 11387, r2
    r2 = part_2(data)
    assert r2 == 37598910447546, r2
