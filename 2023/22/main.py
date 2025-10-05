# https://adventofcode.com/2023/day/22
# --- Day 22: Sand Slabs ---

import uuid
from collections import defaultdict
from dataclasses import dataclass
from typing import Tuple, List

from helpers.utils import (
	read_input_from_main,
    flatten,
    Colors
)

TEST_INPUT = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""

@dataclass
class Brick:
    id: str|uuid.UUID
    start: Tuple[int, ...]
    end: Tuple[int, ...]
    z: int
    x_span: int
    y_span: int
    z_span: int

    def __init__(self, id: str|uuid.UUID, start: Tuple[int, ...], end: Tuple[int, ...], z: int):
        self.id = id
        self.start = start
        self.end = end
        self.z = z
        self.x_span = end[0] - start[0] + 1
        self.y_span = end[1] - start[1] + 1
        self.z_span = end[2] - start[2] + 1

    def will_collide(self, other: "Brick") -> bool:
        """Check if this brick collides with another brick."""
        if self.z-1 < other.z + other.z_span and self.z-1 + self.z_span > other.z:
            if not (self.end[0] < other.start[0] or self.start[0] > other.end[0] or
                    self.end[1] < other.start[1] or self.start[1] > other.end[1]):
                return True
        return False

def print_stack(bricks, axis='x'):
    axis_idx = 0 if axis == 'x' else 1
    max_z_actual = max(brick.z + brick.z_span for brick in bricks)
    max_axis = max(brick.end[axis_idx] for brick in bricks)

    matrix = [[' . ' for _ in range(max_axis + 1)] for _ in range(max_z_actual + 1)]

    colors = [Colors.red, Colors.green, Colors.purple]
    for brick in bricks:
        c = colors[hash(brick.id) % len(colors)]
        for x in range(brick.start[axis_idx], brick.end[axis_idx] + 1):
            for z in range(brick.z, brick.z + brick.z_span):
                matrix[max_z_actual-z][x] = c((str(brick.id) + ' ')[:2]).strip()

    print(f"{axis}/z :".upper())
    for z in range(max_z_actual + 1):
        print(' '.join(matrix[z]), max_z_actual - z)


def parse_input(lines: List[str]) -> List[Brick]:
    bricks = []
    for i, line in enumerate(lines):
        start, end = [tuple(map(int, s.split(','))) for s in line.split('~')]
        bricks.append(Brick(id=uuid.uuid4() if len(lines) > 26 else chr(65+i), start=start, end=end, z=start[2]))
    bricks.sort(key=lambda b: b.end[2])
    return bricks


def simulate_gravity(bricks: List[Brick]) -> Tuple[List[Brick], dict, dict]:
    # Simulate gravity
    bricks_above = {}
    bricks_below = {}
    dropped_at_z = defaultdict(list)  # bricks at each z level
    for brick in bricks:
        bricks_above.setdefault(brick.id, [])
        bricks_below.setdefault(brick.id, [])
        while brick.z > 0:
            below = list(filter(lambda x: x.id != brick.id and brick.will_collide(x), dropped_at_z[brick.z]))
            # If there is at least one brick below, stop
            if len(below):
                for b in below:
                    bricks_above[b.id].append(brick.id)
                    bricks_below[brick.id].append(b.id)
                break

            brick.z -= 1

        dropped_at_z[brick.z + brick.z_span].append(brick)

    return bricks, bricks_above, bricks_below

def can_be_desintegrated(bricks, bricks_above):
    # A brick can be desintegrated if all bricks above it can be supported by other bricks
    return list(brick.id for brick in bricks if set(flatten([list(set(bricks_above[k]) & set(bricks_above[brick.id])) for k in bricks_above if k != brick.id])) == set(bricks_above[brick.id]))


def part1(lines):
    # Simulate gravity
    bricks, bricks_above, _ = simulate_gravity(parse_input(lines))

    # For each brick, count how many bricks are supporting it
    # a brick A supports brick B if A is directly below B
    # search if all supported bricks can be supported by other bricks
    # if yes, count it as it can be disintegrated
    return len(can_be_desintegrated(bricks, bricks_above))

def part2(lines):
    # Simulate gravity
    bricks, bricks_above, bricks_below = simulate_gravity(parse_input(lines))

    def fall_from(brick_id, fallen = tuple()):
        """
        The function fall_from recursively computes all brick IDs that would fall in a chain reaction
        if the brick with brick_id falls, considering dependencies between bricks (those above and below).

        It uses a cache to optimize recursive calls.
        At each step, it adds to the fallen list the bricks that can fall because all their supporting bricks have already fallen.
        It returns the final list of fallen bricks starting from the initial brick.
        """
        for ab in bricks_above[brick_id]:
            if all(ab in fallen for ab in bricks_below[ab] if ab != brick_id):
                fallen = fall_from(ab, fallen + tuple([ab]))

        return fallen

    g = can_be_desintegrated(bricks, bricks_above)

    # Count chaining fallen bricks for each brick that shouldn't be disintegrated from part 1
    return sum(len(fall_from(brick.id)) for brick in bricks if brick.id not in g)


if __name__ == "__main__":
    test_input = TEST_INPUT.splitlines()
    r1 = part1(test_input)
    assert r1 == 5, r1
    data = read_input_from_main(__file__)
    r1 = part1(data)
    assert r1 == 398, r1
    print(f"#1: {r1}")
    r2 = part2(test_input)
    assert r2 == 7, r2
    r2 = part2(data)
    assert r2 == 70727, r2
    print(f"#2: {r2}")
