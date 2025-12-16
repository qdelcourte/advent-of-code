# https://adventofcode.com/2025/day/5
# --- Day 5: Cafeteria ---

from helpers.utils import (
	read_input_from_main
)

TEST_INPUT = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""

def parse(data):
    ingredient_ranges, ingredients, breakline = [], [], False
    for line in data:
        if breakline:
            ingredients.append(int(line))
        elif line == '':
            breakline = True
        else:
            ingredient_ranges.append(tuple(map(int, line.split('-'))))
    return ingredient_ranges, ingredients

def part1(data):
    ingredient_ranges, ingredients = parse(data)

    return len(set(
        ingredient
        for ingredient in ingredients
        for a, b in ingredient_ranges
        if a <= ingredient <= b
    ))

def part2(data):
    ranges, _ = parse(data)

    unions = []
    for begin, end in sorted(ranges):
        if unions and unions[-1][1] >= begin - 1:
            unions[-1][1] = max(unions[-1][1], end)
        else:
            unions.append([begin, end])

    return sum(b+1 - a for a, b in unions)

if __name__ == "__main__":
    test_input = TEST_INPUT.splitlines()
    r1 = part1(test_input)
    assert r1 == 3, r1
    data = read_input_from_main(__file__)
    r1 = part1(data)
    assert r1 == 615, r1
    print(f"#1: {r1}")
    r2 = part2(test_input)
    assert r2 == 14, r2
    r2 = part2(data)
    assert r2 == 353716783056994, r2
    print(f"#2: {r2}")
