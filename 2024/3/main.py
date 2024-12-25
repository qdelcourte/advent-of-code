# https://adventofcode.com/2024/day/3
# --- Day 3: Mull It Over ---

import re

regex = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
regex_2 = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)|(?P<dont>don't\(\))|(?P<do>do\(\))")

TEST_INPUT = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
TEST_INPUT_2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"


def part_1(lines):
    return sum(int(m.group(1)) * int(m.group(2)) for line in lines for m in regex.finditer(line))


def part_2(lines):
    r = 0
    enabled = True
    for line in lines:
        for m in regex_2.finditer(line):
            (o1, o2, dont, do) = m.groups()
            enabled = True if do else False if dont else enabled
            if enabled and o1 and o2:
                r += int(o1) * int(o2)
    return r


if __name__ == '__main__':
    test_input = TEST_INPUT.splitlines()
    r1 = part_1(test_input)
    assert r1 == 161, r1
    data = open('./input.txt', 'r').read().splitlines()
    r1 = part_1(data)
    assert r1 == 180233229, r1
    test_input = TEST_INPUT_2.splitlines()
    r2 = part_2(test_input)
    assert r2 == 48, r2
    r2 = part_2(data)
    assert r2 == 95411583, r2
