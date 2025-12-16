# https://adventofcode.com/2025/day/3
# --- Day 3: Lobby ---

from helpers.utils import (
	read_input_from_main
)

TEST_INPUT = """987654321111111
811111111111119
234234234234278
818181911112111"""

def solve(data, k=12):
    r = 0
    for batteries in data:
        nb, remaining, f, next_index = len(batteries), k, "", -1
        while remaining:
            # Search for the next biggest digit in the allowed remaining window
            j = max(batteries[next_index+1 : nb - remaining+1])
            # Move the index to the found digit
            next_index = batteries.index(j, next_index+1)
            f += j
            remaining -= 1
        r += int(f)

    return r

if __name__ == "__main__":
    test_input = TEST_INPUT.splitlines()
    r1 = solve(test_input, 2)
    assert r1 == 357, r1
    data = read_input_from_main(__file__)
    r1 = solve(data, 2)
    assert r1 == 17031, r1
    print(f"#1: {r1}")
    r2 = solve(test_input, 12)
    assert r2 == 3121910778619, r2
    r2 = solve(data, 12)
    assert r2 == 168575096286051, r2
    print(f"#2: {r2}")
