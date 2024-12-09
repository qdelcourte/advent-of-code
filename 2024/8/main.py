# https://adventofcode.com/2024/day/8
# --- Day 8: Resonant Collinearity ---

from itertools import combinations

import numpy as np

TEST_INPUT = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""


def get_anti_nodes(m, p1, p2):
    a1, a2 = None, None
    if p1:
        a1 = p1[0] - (p2[0] - p1[0]), p1[1] - (p2[1] - p1[1])
        if not (0 <= a1[0] < m.shape[0] and 0 <= a1[1] < m.shape[1]):
            a1 = None
    if p2:
        a2 = p2[0] - (p1[0] - p2[0]), p2[1] - (p1[1] - p2[1])
        if not (0 <= a2[0] < m.shape[0] and 0 <= a2[1] < m.shape[1]):
            a2 = None
    return a1, a2


def part_1(lines):
    m = np.array([list(line) for line in lines], str)

    antennas = {}
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            if m[i][j] != '.':
                antennas.setdefault(str(m[i][j]), []).append((i, j))

    anti_nodes = set()
    for antenna in antennas.keys():
        for pair in combinations(antennas[antenna], 2):
            a1, a2 = get_anti_nodes(m, *pair)
            if a1:
                anti_nodes.add(a1)
            if a2:
                anti_nodes.add(a2)

    return len(anti_nodes)


def part_2(lines):
    m = np.array([list(line) for line in lines], str)

    antennas = {}
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            if m[i][j] != '.':
                antennas.setdefault(str(m[i][j]), []).append((i, j))

    anti_nodes = set()
    for antenna in antennas.keys():
        for pair in combinations(antennas[antenna], 2):
            anti_nodes.update(generate_anti_nodes(m, *pair))

    return len(anti_nodes)


def generate_anti_nodes(m, p1, p2):
    # Generate nodes until bounds
    nodes = set()
    d_0 = p2[0] - p1[0]
    d_1 = p2[1] - p1[1]

    p1_0, p1_1 = p1
    while 0 <= p1_0 < m.shape[0] and 0 <= p1_1 < m.shape[1]:
        nodes.add((p1_0, p1_1))
        p1_0 -= d_0
        p1_1 -= d_1

    p2_0, p2_1 = p2
    while 0 <= p2_0 < m.shape[0] and 0 <= p2_1 < m.shape[1]:
        nodes.add((p2_0, p2_1))
        p2_0 += d_0
        p2_1 += d_1

    return nodes


if __name__ == '__main__':
    test_input = TEST_INPUT.splitlines()
    r1 = part_1(test_input)
    assert r1 == 14, r1
    data = open('./input.txt', 'r').read().splitlines()
    r1 = part_1(data)
    assert r1 == 285, r1
    test_input = TEST_INPUT.splitlines()
    r2 = part_2(test_input)
    assert r2 == 34, r2
    r2 = part_2(data)
    assert r2 == 944, r2
