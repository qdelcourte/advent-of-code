# https://adventofcode.com/2025/day/1
# --- Day 1: Secret Entrance ---

from helpers.utils import (
	read_input_from_main
)

TEST_INPUT = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""

def part1(data):
    pointing, n = 50, 0
    for line in data:
        pointing = (pointing + int(line[1:]) * (1, -1)[line[0] == 'L']) % 100
        if pointing == 0:
            n += 1
    return n


def part2(data):
    pointing, n = 50, 0
    for line in data:
        for _ in range(int(line[1:])):
            pointing = (pointing + (1, -1)[line[0] == 'L']) % 100
            if pointing == 0:
                n += 1
    return n

if __name__ == "__main__":
    test_input = TEST_INPUT.splitlines()
    r1 = part1(test_input)
    assert r1 == 3, r1
    data = read_input_from_main(__file__)
    r1 = part1(data)
    assert r1 == 1089, r1
    print(f"#1: {r1}")
    r2 = part2(test_input)
    assert r2 == 6, r2
    r2 = part2("R1000".splitlines())
    assert r2 == 10, r2
    r2 = part2(data)
    assert r2 == 6530, r2
    print(f"#2: {r2}")
