# https://adventofcode.com/2022/day/6
# --- Day 6: Tuning Trouble ---

TEST_INPUT = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"


def solve(data, size=4):
    for i, _ in enumerate(data):
        if len(set(data[i:i+size])) == size:
            return i + size
    return None

if __name__  == '__main__':
    r1 = solve(TEST_INPUT)
    assert r1 == 7, r1
    data = open('./input.txt').read()
    r1 = solve(data)
    assert r1 == 1987, r1
    r2 = solve(TEST_INPUT, size=14)
    assert r2 == 19, r2
    r2 = solve(data, size=14)
    assert r2 == 3059, r2
