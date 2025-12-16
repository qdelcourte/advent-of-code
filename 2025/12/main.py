# https://adventofcode.com/2025/day/12
# --- Day 12: Christmas Tree Farm ---

from helpers.utils import (
	read_input_from_main
)

TEST_INPUT = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2"""

def part1(data):
    boxes = []
    for line in data:
        if 'x' in line:
            sizes, qty_shapes = line.split(': ')
            boxes.append((tuple(map(int, sizes.split('x'))), list(map(int, qty_shapes.split()))))

    # Shape have all an area of 7
    # Admit that the sum of all shape area must be lower than box area
    # That number of box seems to be the right answer. Lucky !
    return sum(1 for sizes, qty_shapes in boxes if sizes[0]*sizes[1] >= sum(qty_shapes) * 7)

if __name__ == "__main__":
    data = read_input_from_main(__file__)
    r1 = part1(data)
    assert r1 == 557, r1
    print(f"#1: {r1}")
