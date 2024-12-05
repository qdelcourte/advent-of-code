# https://adventofcode.com/2024/day/1
# --- Day 1: Historian Hysteria ---

TEST_INPUT = """3   4
4   3
2   5
1   3
3   9
3   3"""


def parse(data):
    left_list = []
    right_list = []
    for line in data:
        [l, r] = line.split('  ')
        left_list.append(int(l))
        right_list.append(int(r))

    return left_list, right_list


def part_1(lines):
    left_list, right_list = parse(lines)
    return sum([abs(left - right) for (left, right) in zip(sorted(left_list), sorted(right_list))])


def part_2(lines):
    left_list, right_list = parse(lines)
    return sum([left * right_list.count(left) for left in left_list])


if __name__ == '__main__':
    test_input = TEST_INPUT.splitlines()
    r1 = part_1(test_input)
    assert r1 == 11, r1
    data = open('./input.txt', 'r').read().splitlines()
    r1 = part_1(data)
    assert r1 == 2176849, r1
    r2 = part_2(test_input)
    assert r2 == 31, r2
    r2 = part_2(data)
    assert r2 == 23384288, r2
