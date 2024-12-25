# https://adventofcode.com/2024/day/12
# --- Day 12: Garden Groups ---

from collections import deque, defaultdict

TEST_INPUT = """AAAA
BBCD
BBCC
EEEC"""

TEST_INPUT_2 = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""

TEST_INPUT_3 = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""


TEST_INPUT_4 = """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE"""

TEST_INPUT_5 = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""


def solve(lines, part2=False):
    areas = defaultdict(int)
    perimeters = defaultdict(int)
    sides = defaultdict(int)
    n_lines = len(lines)

    queue = deque([((0, 0), None)])
    visited = set()
    n_regions = 0
    region = None

    dirs = {
        'UL': (-1, -1),
        'UR': (-1, +1),
        'DL': (+1, -1),
        'DR': (+1, +1),
        'L': (0, -1),
        'R': (0, +1),
        'U': (-1, 0),
        'D': (+1, 0),
    }

    while queue:
        plant, prev_region = queue.popleft()
        if plant in visited:
            continue
        visited.add(plant)

        y, x = plant
        if prev_region is None:
            n_regions += 1
            region = (lines[y][x], ++n_regions)

        n = 0
        cells = {}
        next_neighbors = []
        other_neighbors = []
        for d, (dy, dx) in dirs.items():
            ny, nx = y + dy, x + dx
            if ny < 0 or nx < 0 or ny >= n_lines or nx >= n_lines:
                cells[d] = None
                continue
            cells[d] = lines[ny][nx]
            if d not in ['U', 'D', 'L', 'R']:
                continue
            if lines[ny][nx] == lines[y][x]:
                n += 1
                if (ny, nx) not in visited:
                    next_neighbors.append(((ny, nx), region))
            elif (ny, nx) not in visited:
                other_neighbors.append(((ny, nx), None))

        queue.extendleft(next_neighbors)
        queue.extend(other_neighbors)

        corner = 0
        plant = lines[y][x]
        if cells['UR'] != plant and cells['U'] == plant and cells['R'] == plant:
            corner += 1
        if cells['U'] != plant and cells['R'] != plant:
            corner += 1

        if cells['UL'] != plant and cells['U'] == plant and cells['L'] == plant:
            corner += 1
        if cells['U'] != plant and cells['L'] != plant:
            corner += 1

        if cells['DL'] != plant and cells['D'] == plant and cells['L'] == plant:
            corner += 1
        if cells['D'] != plant and cells['L'] != plant:
            corner += 1

        if cells['DR'] != plant and cells['D'] == plant and cells['R'] == plant:
            corner += 1
        if cells['D'] != plant and cells['R'] != plant:
            corner += 1

        perimeter = 4 - n
        perimeters[region] += perimeter
        areas[region] += 1
        sides[region] += corner

    if part2:
        return sum(areas[region] * sides[region] for region in areas.keys())
    return sum(areas[region] * perimeters[region] for region in areas.keys())


if __name__ == '__main__':
    test_input = TEST_INPUT.splitlines()
    t1 = solve(test_input)
    assert t1 == 140, t1
    test_input_2 = TEST_INPUT_2.splitlines()
    t2 = solve(test_input_2)
    assert t2 == 772, t2
    test_input_3 = TEST_INPUT_3.splitlines()
    t3 = solve(test_input_3)
    assert t3 == 1930, t3
    data = open('./input.txt', 'r').read().splitlines()
    r1 = solve(data)
    assert r1 == 1446042, r1
    t1 = solve(test_input, part2=True)
    assert t1 == 80, t1
    t2 = solve(test_input_2, part2=True)
    assert t2 == 436, t2
    t3 = solve(test_input_3, part2=True)
    assert t3 == 1206, t3
    test_input_4 = TEST_INPUT_4.splitlines()
    t4 = solve(test_input_4, part2=True)
    assert t4 == 236, t4
    test_input_5 = TEST_INPUT_5.splitlines()
    t5 = solve(test_input_5, part2=True)
    assert t5 == 368, t5
    r2 = solve(data, part2=True)
    assert r2 == 902742, r2
