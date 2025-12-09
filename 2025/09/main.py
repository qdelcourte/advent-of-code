# https://adventofcode.com/2025/day/9
# --- Day 9: Movie Theater ---

import heapq
from functools import cache
from itertools import combinations

from helpers.utils import (
	read_input_from_main
)

TEST_INPUT = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""

def area(a, b): return (abs(b[0] - a[0]) + 1) * (abs(b[1] - a[1]) + 1)

def part1(data):
    return max(area(a, b) for a, b in combinations([tuple(map(int, l.split(','))) for l in data], 2))

def is_point_in_segment(px, py, x1, y1, x2, y2):
    if x1 == x2:
        return px == x1 and min(y1, y2) <= py <= max(y1, y2) # vertical segment
    return py == y1 and min(x1, x2) <= px <= max(x1, x2) # horizontal segment

@cache
def is_point_in_polygon(point, polygon):
    """Ray casting"""
    inside = False

    for (xA, yA), (xB, yB) in zip(polygon, polygon[1:] + polygon[:1]):
        if is_point_in_segment(*point, *(xA, yA), *(xB, yB)):
            return True

        if (
            ((yA > point[1]) != (yB > point[1]))
            and (point[0] < (xB - xA) * (point[1] - yA) / (yB - yA) + xA)
        ):
            inside = not inside

    return inside

@cache
def segment_in_polygon(x1, y1, x2, y2, polygon):
    # Check that the ends are inside
    if not (is_point_in_polygon((x1, y1), polygon) and is_point_in_polygon((x2, y2), polygon)):
        return False

    if y1 == y2:
        xmin, xmax = sorted([x1, x2])
        for (xA, yA), (xB, yB) in zip(polygon, polygon[1:] + polygon[:1]):
            # Vertical Edge intersect segment - strictly because border count as inside
            if xA == xB and xmin < xA < xmax and min(yA, yB) < y1 < max(yA, yB):
                return False

    elif x1 == x2:
        ymin, ymax = sorted([y1, y2])
        for (xA, yA), (xB, yB) in zip(polygon, polygon[1:] + polygon[:1]):
            # Horizontal Edge intersect segment - strictly because border count as inside
            if yA == yB and ymin < yA < ymax and min(xA, xB) < x1 < max(xA, xB):
                return False
    else:
        return False

    return True

def part2(data):
    tiles = tuple([tuple(map(int, l.split(','))) for l in data])

    # Generate combinations with largest area first - first area in polygon is the result
    combs = list(heapq.nlargest(
        len(tiles)*len(tiles),
        (((a, b), area(a, b)) for a, b in combinations(tiles, 2)),
        key=lambda x: x[1]
    ))

    for (a, b), c_area in combs:
        if a[1] == b[1] or a[0] == b[0]: continue
        edges = [(*a, *(b[0], a[1])), (*(b[0], a[1]), *b), (*b, *(a[0], b[1])), (*(a[0], b[1]), *a)]
        if all(segment_in_polygon(*edge, tiles) for edge in edges):
            return c_area
    return None

if __name__ == "__main__":
    test_input = TEST_INPUT.splitlines()
    r1 = part1(test_input)
    assert r1 == 50, r1
    data = read_input_from_main(__file__)
    r1 = part1(data)
    assert r1 == 4715966250, r1
    print(f"#1: {r1}")
    r2 = part2(test_input)
    assert r2 == 24, r2
    r2 = part2(data)
    assert r2 == 1530527040, r2
    print(f"#2: {r2}")
