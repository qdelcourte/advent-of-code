# https://adventofcode.com/2024/day/10
# --- Day 10: Hoof It ---

from collections import deque
import numpy as np

TEST_INPUT = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""


def trail_pathfinding(m, _from=None):
    step_checked = set()
    valid_trails = []
    trail = deque([(None, _from)])
    while trail:
        prev, curr = trail.popleft()
        step_checked.add((prev, curr))
        prev_step = -1 if prev is None else m[prev]

        y, x = curr
        if y < 0 or x < 0 or y >= m.shape[0] or x >= m.shape[1]:
            continue

        step = m[curr]
        if step - prev_step == 1:
            if step == 9:
                valid_trails.append(curr)
                continue
            next_steps = [(curr, (y - 1, x)), (curr, (y + 1, x)), (curr, (y, x - 1)), (curr, (y, x + 1))]
            for next_step in next_steps:
                if next_step not in step_checked:
                    trail.append(next_step)

    return valid_trails


def part_1(lines):
    m = np.array([list(line) for line in lines], int)

    return sum(len(set(trail_pathfinding(m, trailhead))) for trailhead in list(zip(*np.where(m == 0))))


def part_2(lines):
    m = np.array([list(line) for line in lines], int)

    return sum(len(trail_pathfinding(m, trailhead)) for trailhead in list(zip(*np.where(m == 0))))


if __name__ == '__main__':
    test_input = TEST_INPUT.splitlines()
    r1 = part_1(test_input)
    assert r1 == 36, r1
    data = open('./input.txt', 'r').read().splitlines()
    r1 = part_1(data)
    assert r1 == 548, r1
    r2 = part_2(test_input)
    assert r2 == 81, r2
    r2 = part_2(data)
    assert r2 == 1252, r2
