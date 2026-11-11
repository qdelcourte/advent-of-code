# https://adventofcode.com/2022/day/9
# --- Day 9: Rope Bridge ---

from helpers.utils import read_input_from_main

TEST_INPUT = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

TEST_INPUT2 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

DIRS = {'R': (1, 0), 'L': (-1, 0), 'U': (0, 1), 'D': (0, -1)}

def solve(data, nb_knots=2):
    # Parse motions
    motions = [(DIRS[line[0]], int(line.split()[1])) for line in data]

    # Index 0 is head and last index is tail
    knots: list[tuple[int, int]] = [(0,0) for _ in range(nb_knots)]

    seen = set()
    for (dx, dy), steps in motions:
        for _ in range(steps):
            knots[0] = (knots[0][0] + dx, knots[0][1] + dy)

            for k in range(nb_knots-1):
                diffx, diffy = knots[k][0] - knots[k+1][0], knots[k][1] - knots[k+1][1]
                if max(abs(diffx), abs(diffy)) >= 2:
                    # Move one step closer in neighbor direction if at least 2 step away
                    knots[k+1] = (
                        knots[k+1][0] + (diffx//abs(diffx) if diffx else 0),
                        knots[k+1][1] + (diffy//abs(diffy) if diffy else 0)
                    )

            # Register tail position
            seen.add(knots[-1])

    return len(seen)

if __name__ == "__main__":
    r1 = solve(TEST_INPUT.splitlines(), nb_knots=2)
    assert r1 == 13, r1
    data = read_input_from_main(__file__)
    r1 = solve(data, nb_knots=2)
    assert r1 == 6642, r1
    print(f"#1: {r1}")
    r2 = solve(TEST_INPUT2.splitlines(), nb_knots=10)
    assert r2 == 36, r2
    r2 = solve(data, nb_knots=10)
    assert r2 == 2765, r2
    print(f"#2: {r2}")
