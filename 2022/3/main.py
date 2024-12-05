# https://adventofcode.com/2022/day/3
# --- Day 3: Rucksack Reorganization ---

TEST_INPUT = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""


def c(c):
    return ord(c) - (38 if c.isupper() else 96)


def part_1(lines):
    return sum(c(list(set(line[:len(line) // 2]).intersection(line[len(line) // 2:]))[0]) for line in lines)


def part_2(lines, nb_elves=3):
    return sum(
        c(list(set(group[0]).intersection(*group[1:nb_elves]))[0])
        for group in zip(*[iter(lines)] * nb_elves)
    )


if __name__ == '__main__':
    test_lines = TEST_INPUT.splitlines()
    t1 = part_1(test_lines)
    assert t1 == 157, t1
    lines = open('./input.txt', 'r').read().splitlines()
    r1 = part_1(lines)
    assert r1 == 7863, r1
    t2 = part_2(test_lines)
    assert t2 == 70, t2
    r2 = part_2(lines)
    assert r2 == 2488, r2
