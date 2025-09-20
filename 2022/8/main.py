# https://adventofcode.com/2022/day/8
# --- Day 8: Treetop Tree House ---

from math import prod

from helpers.utils import str_to_matrix, read_input_from_main

TEST_INPUT = """30373
25512
65332
33549
35390"""

def part1(data):
    m = str_to_matrix(data)

    nb_visible = 0
    for y, line in enumerate(m):
        for x, value in enumerate(line):
            top = list(map(lambda l: l[x], m[:y]))
            bottom = list(map(lambda l: l[x], reversed(m[y+1:])))
            left = m[y][:x]
            right = list(reversed(m[y][x+1:]))

            if not all(map(lambda c: len(list(filter(lambda v: v >= value, c))) != 0, [top, bottom, left, right])):
                nb_visible += 1
                continue

    return nb_visible


def part2(data, trees = None):
    if trees is None:
        trees = []

    m = str_to_matrix(data)

    def c(value, top, bottom, left, right):
        def collect_until(seq):
            result = []
            for x in seq:
                result.append(x)
                if x >= value:
                    break
            return result
        return [collect_until(top), collect_until(bottom), collect_until(left), collect_until(right)]

    dataset = []
    for y, line in enumerate(m):
        for x, value in enumerate(line):
            if trees and (x,y) not in trees:
                continue
            top = list(map(lambda l: l[x], reversed(m[:y])))
            bottom = list(map(lambda l: l[x], m[y+1:]))
            left = list(reversed(m[y][:x]))
            right = list(m[y][x+1:])

            dataset.append(prod(map(lambda x: len(x), c(value, top, bottom, left, right))))

    return max(dataset)


if __name__ == "__main__":
    test_input = TEST_INPUT.splitlines()
    r1 = part1(test_input)
    assert r1 == 21, r1
    data = read_input_from_main(__file__)
    r1 = part1(data)
    assert r1 == 1807, r1
    print(f"#1: {r1}")
    r21 = part2(test_input, trees=[(2,1)])
    assert r21 == 4, r21
    r22 = part2(test_input, trees=[(2,1), (2,3)])
    assert r22 == 8, r22
    r2 = part2(data)
    assert r2 == 480000, r2
    print(f"#2: {r2}")
