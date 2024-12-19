# https://adventofcode.com/2024/day/19
# --- Day 19: Linen Layout ---

from functools import cache

TEST_INPUT = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""


def parse(lines):
    patterns, designs = [], []
    for i, line in enumerate(lines):
        if i == 0:
            patterns = line.split(', ')
        elif i > 1:
            designs.append(line)
    return patterns, designs


def part_1(lines):
    patterns, designs = parse(lines)

    def search(d, start=0):
        """
        Can do it recursively against each patterns
        For a design, search a pattern who match the start
        then continue to match a pattern after that start, etc... until the full match
        """
        if len(d) == start:
            return True

        for pattern in patterns:
            if d[start:].startswith(pattern) and search(d, start + len(pattern)):
                return True

    return len([design for design in designs if (search(design) or 0) > 0])


def part_2(lines):
    patterns, designs = parse(lines)

    @cache
    def search(d, start=0):
        if len(d) == start:
            return 1
        return sum(
            search(d, start + len(pattern))
            for pattern in patterns
            if d[start:].startswith(pattern))

    return sum(map(search, designs))


if __name__ == '__main__':
    test_input = TEST_INPUT.splitlines()
    r1 = part_1(test_input)
    assert r1 == 6, r1
    data = open('./input.txt', 'r').read().splitlines()
    r1 = part_1(data)
    assert r1 == 285, r1
    r2 = part_2(test_input)
    assert r2 == 16, r2
    r2 = part_2(data)
    assert r2 == 636483903099279, r2
