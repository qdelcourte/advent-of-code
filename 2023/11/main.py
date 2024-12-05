# https://adventofcode.com/2023/day/11
# --- Day 11: Cosmic Expansion ---
import re
from itertools import combinations


def column(x, i):
    return [l[i] for l in x]


def expansion(m):
    expanded_galaxy = []
    for i, row in enumerate(m):
        expanded_galaxy.append(row)
        if '#' not in row:
            expanded_galaxy.append(row)

    columns_no_galaxies = []
    for i in range(0, len(m[0])):
        if '#' not in column(m, i):
            columns_no_galaxies.append(i)

    for i, n in enumerate(columns_no_galaxies):
        for k, r in enumerate(expanded_galaxy):
            expanded_galaxy[k] = r[:n + i] + '.' + r[n + i:]

    return expanded_galaxy


def total_shortest_paths(m):
    expanded_galaxy = expansion(m)

    galaxies = set()
    for i, line in enumerate(expanded_galaxy):
        for g in re.finditer(r'#', line):
            galaxies.add((g.start(), i))

    result = 0
    for pair in list(combinations(galaxies, 2)):
        left, right = pair
        result += abs(left[0]-right[0]) + abs(left[1] - right[1])

    return result


def test_1():
    # Test expansion
    m = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""".splitlines()
    return total_shortest_paths(m)


def part_1():
    return total_shortest_paths(data)


def test_2():
    lines = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""".splitlines()

    return solve(lines, 100)


def part_2():
    return solve(data, 1000000)


def solve(data, expand_factor: int = 2):
    rows_no_galaxies = []
    for i, row in enumerate(data):
        if '#' not in row:
            rows_no_galaxies.append(i)

    columns_no_galaxies = []
    for i in range(0, len(data[0])):
        if '#' not in column(data, i):
            columns_no_galaxies.append(i)

    galaxies = set()
    for i, line in enumerate(data):
        for g in re.finditer(r'#', line):
            galaxies.add((g.start(), i))

    def count_elements_between(value1, value2, elements):
        return sum(1 for elem in elements if value1 > elem > value2 or value2 > elem > value1)

    def calculate_expanded(expand_factor, nre, nce):
        return (expand_factor * nre) - nre + (expand_factor * nce) - nce if nre > 0 or nce > 0 else 0

    result = 0
    for pair in list(combinations(galaxies, 2)):
        left, right = pair

        nb_rows_expanded = count_elements_between(left[1], right[1], rows_no_galaxies)
        nb_cols_expanded = count_elements_between(left[0], right[0], columns_no_galaxies)
        expanded = calculate_expanded(expand_factor, nb_rows_expanded, nb_cols_expanded)

        # |Lx - Rx| + |Ly - Ry|
        # + (expand_factor * nbColsExpanded - nbColsExpanded) + (expand_factor * nbRowsExpanded - nbRowsExpanded)
        result += (abs(left[0] - right[0]) + abs(left[1] - right[1])) + expanded

    return result


if __name__ == '__main__':
    t1 = test_1()
    assert t1 == 374, t1
    data = open('./input.txt', 'r').read().splitlines()
    r1 = part_1()
    assert r1 == 9647174, r1
    print(f"#1: {r1}")
    t2 = test_2()
    assert t2 == 8410, t2
    r2 = part_2()
    assert r2 == 377318892554, r2
    print(f"#2: {r2}")
