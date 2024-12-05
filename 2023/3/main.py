# https://adventofcode.com/2023/day/3
# --- Day 3: Gear Ratios ---

import re
from functools import reduce


def part_1():
    n_lines = len(lines)

    result = 0
    for i, line in enumerate(lines):
        for m in re.finditer(r'\d+', line):
            start, end = max(m.start()-1, 0), min(m.end()+1, len(line))
            to_valid = (
                line[start:end]
                + (lines[i - 1][start:end] if i - 1 >= 0 else '')
                + (lines[i + 1][start:end] if i + 1 < n_lines else ''))
            if re.search(r'[^\d.]', to_valid):
                result += int(m.group(0))

    return result


def part_2():
    """
    Compute with coordinates for fun :)
    multiply numbers with a common gear (in the same coordinates)
    """
    n_lines = len(lines)
    indexed_part_numbers_with_gear = {}
    for i, line in enumerate(lines):
        for m in re.finditer(r'\d+', line):
            start, end = max(m.start()-1, 0), min(m.end()+1, len(line))
            to_valid = (
                (lines[i - 1][start:end] if i - 1 >= 0 else '')
                + line[start:end]
                + (lines[i + 1][start:end] if i + 1 < n_lines else ''))
            if re.search(r'[^\d.]', to_valid):
                try:
                    gear_index = to_valid.index('*')
                    group_size = end - start
                    x1 = gear_index - (int(gear_index/group_size))*group_size + start - 1
                    y1 = max(i + int(gear_index/group_size) - 1, 1)

                    indexed_part_numbers_with_gear.setdefault((x1, y1), [])
                    indexed_part_numbers_with_gear[(x1, y1)].append(int(m.group(0)))
                except ValueError:
                    pass

    return reduce(lambda a, b: a+(b[0]*b[1] if len(b) == 2 else 0), indexed_part_numbers_with_gear.values(), 0)


if __name__ == '__main__':
    lines = open('./input.txt', 'r').read().splitlines()
    r1 = part_1()
    assert r1 == 527446, r1
    print(f"#1: {r1}")
    r2 = part_2()
    assert r2 == 73201705, r2
    print(f"#2: {r2}")
