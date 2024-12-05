# https://adventofcode.com/2023/day/10
# --- Day 10: Pipe Maze ---

import sys


def get_s_coord(lines):
    for i, line in enumerate(lines):
        if 'S' in line:
            return line.index('S'), i


def test_1():
    example = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""

    lines = example.splitlines()
    nb_lines = len(lines)
    line_len = len(lines[0])
    x_pos, y_pos = get_s_coord(lines)

    seen = set()

    def search_paths(x, y, depth=1):
        if (x, y) in seen or (pipe := lines[y][x]) == 'S' and depth > 1:
            return depth
        seen.add((x, y))
        depths = []
        if x + 1 < line_len:
            adjacent = lines[y][x+1]
            if pipe in 'S-FL' and adjacent in 'J-7' and (x+1, y) not in seen:
                # Right good
                depths.append(search_paths(x + 1, y, depth + 1))
        if x - 1 >= 0:
            adjacent = lines[y][x-1]
            if pipe in 'S-J7' and adjacent in '-FL' and (x-1, y) not in seen:
                # Left good
                depths.append(search_paths(x - 1, y, depth + 1))
        if y - 1 >= 0:
            adjacent = lines[y-1][x]
            if pipe in 'S|JL' and adjacent in '|7F' and (x, y-1) not in seen:
                # Top good
                depths.append(search_paths(x, y - 1, depth + 1))
        if y + 1 < nb_lines:
            adjacent = lines[y+1][x]
            if pipe in 'S|7F' and adjacent in '|JL' and (x, y+1) not in seen:
                # Bottom good
                depths.append(search_paths(x, y + 1, depth + 1))
        return max(depths) if len(depths) else depth

    return search_paths(x_pos, y_pos) // 2


def part_1():
    nb_lines = len(lines)
    line_len = len(lines[0])
    x_pos, y_pos = get_s_coord(lines)

    seen = set()
    sys.setrecursionlimit(20000)

    def search_paths(x, y, depth=1):
        if (x, y) in seen or ((pipe := lines[y][x]) == 'S' and depth > 1):
            return depth
        seen.add((x, y))
        depths = []
        if x + 1 < line_len:
            adjacent = lines[y][x+1]
            if pipe in 'S-FL' and adjacent in 'J-7' and (x+1, y) not in seen:
                # Right good
                depths.append(search_paths(x + 1, y, depth + 1))
        if x - 1 >= 0:
            adjacent = lines[y][x-1]
            if pipe in 'S-J7' and adjacent in '-FL' and (x-1, y) not in seen:
                # Left good
                depths.append(search_paths(x - 1, y, depth + 1))
        if y - 1 >= 0:
            adjacent = lines[y-1][x]
            if pipe in 'S|JL' and adjacent in '|7F' and (x, y-1) not in seen:
                # Top good
                depths.append(search_paths(x, y - 1, depth + 1))
        if y + 1 < nb_lines:
            adjacent = lines[y+1][x]
            if pipe in 'S|7F' and adjacent in '|JL' and (x, y+1) not in seen:
                # Bottom good
                depths.append(search_paths(x, y + 1, depth + 1))
        return max(depths) if len(depths) else depth

    return search_paths(x_pos, y_pos) // 2


def solve_2(lines):
    nb_lines = len(lines)
    line_len = len(lines[0])
    x_pos, y_pos = get_s_coord(lines)

    seen = set()

    def search_paths(x, y):
        pipe = lines[y][x]
        seen.add((x, y))
        while pipe != 'S' or len(seen) == 1:
            if x + 1 < line_len:
                adjacent = lines[y][x + 1]
                if pipe in 'S-FL' and adjacent in 'SJ-7' and (
                        (x + 1, y) not in seen or (adjacent == 'S' and len(seen) > 2)):
                    # Right good
                    pipe = adjacent
                    seen.add((x + 1, y))
                    x += 1
                    continue
            if x - 1 >= 0:
                adjacent = lines[y][x - 1]
                if pipe in 'S-J7' and adjacent in 'S-FL' and (
                        (x - 1, y) not in seen or (adjacent == 'S' and len(seen) > 2)):
                    # Left good
                    pipe = adjacent
                    seen.add((x - 1, y))
                    x -= 1
                    continue
            if y - 1 >= 0:
                adjacent = lines[y - 1][x]
                if pipe in 'S|JL' and adjacent in 'S|7F' and (
                        (x, y - 1) not in seen or (adjacent == 'S' and len(seen) > 2)):
                    # Top good
                    pipe = adjacent
                    seen.add((x, y - 1))
                    y -= 1
                    continue
            if y + 1 < nb_lines:
                adjacent = lines[y + 1][x]
                if pipe in 'S|7F' and adjacent in 'S|JL' and (
                        (x, y + 1) not in seen or (adjacent == 'S' and len(seen) > 2)):
                    # Bottom good
                    pipe = adjacent
                    seen.add((x, y + 1))
                    y += 1
                    continue

    search_paths(x_pos, y_pos)

    keep = set()
    for i, line in enumerate(lines):
        for x in range(0, len(line)):
            if (x, i) not in seen:
                c = 0
                prev_bend = None
                for k in range(x + 1, len(line)):
                    if (k, i) not in seen:
                        continue

                    if lines[i][k] in 'LF' and prev_bend is None:
                        prev_bend = lines[i][k]
                    elif prev_bend and prev_bend in 'LF' and lines[i][k] == '-':
                        pass
                    elif prev_bend == 'L':
                        if lines[i][k] == '7':
                            c += 1
                        prev_bend = None
                    elif prev_bend == 'F':
                        if lines[i][k] == 'J':
                            c += 1
                        prev_bend = None
                    elif lines[i][k] == '|':
                        c += 1

                if c % 2 != 0:
                    keep.add((x, i))

    return len(keep)


def test_2():
    # Assert 10
    lines = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L""".splitlines()
    # Assert 8
#     lines = """.F----7F7F7F7F-7....
# .|F--7||||||||FJ....
# .||.FJ||||||||L7....
# FJL7L7LJLJ||LJ.L-7..
# L--J.L7...LJS7F-7L7.
# ....F-J..F7FJ|L7L7L7
# ....L7.F7||L7|.L7L7|
# .....|FJLJ|FJ|F7|.LJ
# ....FJL-7.||.||||...
# ....L---J.LJ.LJLJ...""".splitlines()
    # Assert 4
#     lines = """...........
# .S-------7.
# .|F-----7|.
# .||.....||.
# .||.....||.
# .|L-7.F-J|.
# .|..|.|..|.
# .L--J.L--J.
# ...........""".splitlines()
    return solve_2(lines)


def part_2():
    return solve_2(lines)


if __name__ == '__main__':
    t1 = test_1()
    assert t1 == 8, t1
    lines = open('./input.txt', 'r').read().splitlines()
    r1 = part_1()
    assert r1 == 6890, r1
    print(f"#1: {r1}")
    t2 = test_2()
    assert t2 == 10, t2
    r2 = part_2()
    assert r2 == 453, r2
    print(f"#2: {r2}")
