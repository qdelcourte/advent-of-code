# https://adventofcode.com/2024/day/11
# --- Day 11: Plutonian Pebbles ---

from collections import Counter
from functools import cache

TEST_INPUT = "125 17"


@cache
def transform(stone):
    if stone == 0:
        return [1]
    elif (stone_len := len(str(stone))) % 2 == 0:
        c = pow(10, stone_len / 2)
        return [int(stone // c), int(stone % c)]
    else:
        return [stone * 2024]


def solve(data, blink=25):
    stones = list(map(int, data.split()))
    for _ in range(blink):
        new_stones = []
        for stone in stones:
            new_stones.extend(transform(stone))
        stones = new_stones

    return len(stones)


def solve2(data, blink=25):
    stones_map = Counter(list(map(int, data.split())))
    for _ in range(blink):
        c = Counter()
        for stone, cnt in stones_map.items():
            c += Counter({
                _stone: _cnt * cnt
                for _stone, _cnt in Counter(transform(stone)).items()
            })
        stones_map = c

    return stones_map.total()


if __name__ == '__main__':
    test_input = TEST_INPUT
    r1 = solve(test_input, 25)
    assert r1 == 55312, r1
    data = open('./input.txt', 'r').readline()
    r1 = solve(data, 25)
    assert r1 == 239714, r1
    r2 = solve2(data, 75)
    assert r2 == 284973560658514, r2
