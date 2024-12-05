# https://adventofcode.com/2022/day/2
# --- Day 2: Rock Paper Scissors ---

TEST_INPUT = """A Y
B X
C Z"""


def get_score(shape, opponent_shape):
    r = 0
    if shape == opponent_shape:
        r += 3
    elif (shape, opponent_shape) in [("A", "C"), ("B", "A"), ("C", "B")]:
        r += 6

    return r + "ABC".index(shape) + 1


def part_1(lines):
    return sum(get_score({"X": "A", "Y": "B", "Z": "C"}.get(line[-1]), line[0]) for line in lines)


def part_2(lines):
    return sum(get_score(
        {
            "X": {"A": "C", "B": "A", "C": "B"}.get(line[0]),
            "Y": line[0],
            "Z": {"A": "B", "B": "C", "C": "A"}.get(line[0])
        }.get(line[-1]), line[0]) for line in lines)


if __name__ == '__main__':
    test_lines = TEST_INPUT.splitlines()
    t1 = part_1(test_lines)
    assert t1 == 15, t1
    lines = open('./input.txt', 'r').read().splitlines()
    r1 = part_1(lines)
    assert r1 == 11475, r1
    t2 = part_2(test_lines)
    assert t2 == 12, t2
    r2 = part_2(lines)
    assert r2 == 16862, r2
