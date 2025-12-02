# https://adventofcode.com/2025/day/2
# --- Day 2: Gift Shop ---

import re

from helpers.utils import (
	read_input_from_main
)

TEST_INPUT = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""

def solve(data, part2=False):
    r = re.compile(r"^(\d+)\1+$" if part2 else r"^(\d+)\1$")

    return sum(
        n
        for start, end in map(lambda s: s.split('-'), data.split(','))
        for n in range(int(start), int(end) + 1)
        if r.search(str(n))
    )

if __name__ == "__main__":
    test_input = TEST_INPUT
    r1 = solve(test_input)
    assert r1 == 1227775554, r1
    data = read_input_from_main(__file__, False)
    r1 = solve(data)
    assert r1 == 40055209690, r1
    print(f"#1: {r1}")
    r2 = solve(test_input, True)
    assert r2 == 4174379265, r2
    r2 = solve(data, True)
    assert r2 == 50857215650, r2
    print(f"#2: {r2}")
