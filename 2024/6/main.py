# https://adventofcode.com/2024/day/6
# --- Day 6: Guard Gallivant ---

from time import perf_counter

import numpy as np

TEST_INPUT = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""


def get_path(m):
    start_pos = tuple(map(int, list(zip(*np.where(m == '^')))[0]))
    visited = [start_pos]
    direction = (-1, 0)

    dirs = {
        (-1, 0): (0, 1),
        (1, 0): (0, -1),
        (0, 1): (1, 0),
        (0, -1): (-1, 0)
    }

    while True:
        next_pos = tuple(map(lambda i, j: i + j, visited[-1], direction))

        if any(map(lambda x: x < 0 or x >= m.shape[0], list(next_pos))):
            break

        front_char = m[*next_pos]
        if front_char == '#':
            direction = dirs[direction]
        else:
            visited.append(next_pos)

    return visited


def part_1(lines):
    return len(set(get_path(np.array([list(line) for line in lines], str))))


def print_array(m):
    for r in range(len(m)):  # rows
        for c in range(len(m[r])):  # columns
            print(m[r][c], " ", sep="", end="")
        print()
    print("-------------")


def part_2(lines):
    d = np.array([list(line) for line in lines], str)
    start_pos = tuple(map(int, list(zip(*np.where(d == '^')))[0]))
    nb_valid_loop = 0

    start_direction = (-1, 0)
    m = np.copy(d)

    dirs = {
        (-1, 0): (0, 1),
        (1, 0): (0, -1),
        (0, 1): (1, 0),
        (0, -1): (-1, 0)
    }

    i = -1
    tic = perf_counter()
    for possible_obstruction_pos in reversed(list(set(get_path(d)[1:]))):
        i += 1
        if i % 100 == 0:
            toc = perf_counter()
            print(f"{i}: ({toc - tic:0.4f} seconds)")

        direction = start_direction
        visited = [(start_pos, direction)]
        visited_set = set(visited)
        while True:
            next_pos = tuple(map(lambda i, j: i + j, visited[-1][0], direction))

            if any(map(lambda x: x < 0 or x >= m.shape[0], list(next_pos))):
                break

            if (next_pos, direction) in visited_set:
                nb_valid_loop += 1
                break

            if m[*next_pos] == '#' or next_pos == possible_obstruction_pos:
                direction = dirs[direction]
            else:
                visited.append((next_pos, direction))
                visited_set.add((next_pos, direction))

    return nb_valid_loop


if __name__ == '__main__':
    test_input = TEST_INPUT.splitlines()
    r1 = part_1(test_input)
    assert r1 == 41, r1
    data = open('./input.txt', 'r').read().splitlines()
    r1 = part_1(data)
    assert r1 == 4454, r1
    r2 = part_2(test_input)
    assert r2 == 6, r2
    r2 = part_2(data)
    assert r2 == 1503, r2
