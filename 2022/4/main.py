# https://adventofcode.com/2022/day/4
# --- Day 4: Camp Cleanup ---

TEST_INPUT = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

def parse(lines):
    for line in lines:
        p1, p2 = list(map(lambda s: list(map(int, s.split('-'))), line.split(',')))
        yield set(range(p1[0], p1[1]+1)), set(range(p2[0], p2[1]+1))
        


def part_1(lines):
    return sum(
        p1.issubset(p2) or p2.issubset(p1)
        for p1, p2 in parse(lines)
    )


def part_2(lines):
    return sum(
        len(p1 & p2) > 0
        for p1, p2 in parse(lines)
    )


if __name__  == '__main__':
    test_input = TEST_INPUT.splitlines()
    r1 = part_1(test_input)
    assert r1 == 2, r1
    data = open('./input.txt').read().splitlines()
    r1 = part_1(data)
    assert r1 == 569, r1
    r2 = part_2(test_input)
    assert r2 == 4, r2
    r2 = part_2(data)
    assert r2 == 936, r2
