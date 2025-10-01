# https://adventofcode.com/2023/day/21
# --- Day 21: Step Counter ---

from collections import deque, defaultdict
from copy import deepcopy

from helpers.utils import read_input_from_main

TEST_INPUT = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""

"""
...........
.....###.#.
.###.##.O#.
.O#O#O.O#..
O.O.#.#.O..
.##O.O####.
.##.O#O..#.
.O.O.O.##..
.##.#.####.
.##O.##.##.
...........
"""

def min_distance(grid, start=None):
    size_grid = len(grid)
    if start is None:
        for row in range(size_grid):
            for col in range(size_grid):
                if grid[row][col] == 'S':
                    start = (row, col)
                    break

    visited = set()
    steps = defaultdict(lambda: 0)

    queue = deque([(start[0], start[1], 0)])
    while queue:
        row, col, dist = queue.popleft()

        if (row, col) in visited:
            continue

        steps[dist] += 1
        visited.add((row, col))

        for d in [(-1, 0), (1, 0), (0, -1), (0, +1)]:
            next_x, next_y = (row + d[0]), (col + d[1])
            if (
                0 <= next_x < size_grid and 0 <= next_y < size_grid
                and grid[next_x][next_y] != '#'
                and (next_x, next_y) not in visited
            ):
                queue.append((next_x, next_y, dist + 1))

    return steps


def part_1(grid, goal):
    return sum([n for d, n in min_distance(deepcopy(grid)).items() if d % 2 == goal % 2 and d <= goal])

def part_2(grid, goal):
    size_grid = len(grid)
    edge = size_grid // 2

    # 26501365 = 65 + (202300 * 131) <=> goal = edge + (N * size_grid)
    n = (goal - edge) // size_grid

    # Full
    full_steps = min_distance(deepcopy(grid))
    even_full = sum([n for d, n in full_steps.items() if d % 2 == 0])
    odd_full = sum([n for d, n in full_steps.items() if d % 2 == 1])

    # Compute from corners: Top left, Bottom left, Bottom right, Top right
    even_corner = odd_corner = 0
    for c in [(0, 0), (size_grid-1, 0), (size_grid-1, size_grid-1), (0, size_grid-1)]:
        steps_c = min_distance(deepcopy(grid), start=c)
        even_corner += sum([n for d, n in steps_c.items() if d % 2 == 0 and d < edge])
        odd_corner += sum([n for d, n in steps_c.items() if d % 2 == 1 and d < edge])

    return (
        (n + 1) ** 2 * odd_full
        + n ** 2 * even_full
        + n * even_corner
        - (n + 1) * odd_corner
    )

if __name__ == '__main__':
    test_grid = [list(line) for line in TEST_INPUT.splitlines()]
    t1_1 = part_1(test_grid, goal=1)
    assert t1_1 == 2, t1_1
    print(f"test 1_1: {t1_1}")
    t1_2 = part_1(test_grid, goal=2)
    assert t1_2 == 4, t1_2
    print(f"test 1_2: {t1_2}")
    t1_3 = part_1(test_grid, goal=3)
    assert t1_3 == 6, t1_3
    print(f"test 1_3: {t1_3}")
    data = read_input_from_main(__file__)
    r1 = part_1([list(line) for line in data], goal=64)
    assert r1 == 3605, r1
    print(f"part 1: {r1}")

    r2 = part_2([list(line) for line in data], goal=26501365)
    assert r2 == 596734624269210, r2
    print(f"part 2: {r2}")
