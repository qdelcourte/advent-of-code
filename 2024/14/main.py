# https://adventofcode.com/2024/day/14
# --- Day 14: Restroom Redoubt ---

import math
from collections import defaultdict

import numpy as np

TEST_INPUT = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""


def pprint_matrix(m):
    for r in range(len(m)):  # rows
        for c in range(len(m[r])):  # columns
            print(m[r][c], " ", sep="", end="")
        print()
    print("-------------")


def parse(lines):
    robots = []
    for line in lines:
        [p, v] = line.split()
        robots.append({
            'p': (int(p.split(',')[0][2:]), int(p.split(',')[1])),
            'v': (int(v.split(',')[0][2:]), int(v.split(',')[1]))
        })
    return robots


def part_1(lines, shape, t):
    quadrants = defaultdict(int)
    for robot in parse(lines):
        [px, py, vx, vy] = [*robot['p'], *robot['v']]
        x, y = ((vx * t) + px) % shape[0], ((vy * t) + py) % shape[1]

        mx, my = shape[0] // 2, shape[1] // 2
        if x < mx and y < my:
            quadrants['UL'] += 1
        elif x > mx and y > my:
            quadrants['DR'] += 1
        elif x > mx and y < my:
            quadrants['UR'] += 1
        elif x < mx and y > my:
            quadrants['DL'] += 1

    return math.prod(quadrants.values())


def part_2(lines, shape):
    """
    What ??
    I don't know, so I tried to find the first position where all robots have a unique position.
    And magically it appears that the fucking tree is here
    """
    m = np.empty((shape[1], shape[0]), dtype=str)
    m.fill('.')

    robots = parse(lines)
    nb_robots = len(robots)
    robots_pos = set()

    # Assume that it needs more than 100 seconds to build that fucking tree
    # so start at 100
    t = 100
    while len(robots_pos) != nb_robots:
        robots_pos.clear()
        for robot in robots:
            [px, py, vx, vy] = [*robot['p'], *robot['v']]
            rx, ry = ((vx * t) + px) % shape[0], ((vy * t) + py) % shape[1]
            if (rx, ry) in robots_pos:
                continue
            robots_pos.add((rx, ry))

        # Try with more seconds ??
        t += 1

    # Draw this fucking tree
    for (x, y) in robots_pos:
        m[y][x] = '#'
    pprint_matrix(m)
    print("Ends with t=", t-1, "seconds and", len(robots_pos), "robots")

    return t-1


if __name__ == '__main__':
    test_input = TEST_INPUT.splitlines()
    r1 = part_1(test_input, shape=(11, 7), t=100)
    assert r1 == 12, r1
    data = open('./input.txt', 'r').read().splitlines()
    r1 = part_1(data, shape=(101, 103), t=100)
    assert r1 == 211773366, r1
    r2 = part_2(data, shape=(101, 103))
    assert r2 == 7344, r2
