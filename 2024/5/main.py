# https://adventofcode.com/2024/day/5
# --- Day 5: Print Queue ---

from functools import cmp_to_key

TEST_INPUT = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""


def parse_input(data):
    [rules_input, updates_input] = data.split('\n\n')
    updates = [list(map(int, x)) for x in map(lambda x: x.split(','), updates_input.splitlines())]
    rules = [tuple(map(int, r)) for rule in rules_input.splitlines() if (r := rule.split('|'))]

    return rules, updates


def cmp(a, b):
    if (a, b) in RULES:
        return -1
    return 1


def is_sorted(update):
    return sorted(update, key=cmp_to_key(cmp)) != update


def part_1(updates):
    return sum(
        up[int((len(up) - 1)/2)]
        for up in updates
        if not is_sorted(up)
    )


def part_2(updates):
    return sum(
        sorted(up, key=cmp_to_key(cmp))[int((len(up) - 1) / 2)]
        for up in updates
        if is_sorted(up)
    )


if __name__ == '__main__':
    test_input = parse_input(TEST_INPUT)
    [RULES, updates] = test_input
    r1 = part_1(updates)
    assert r1 == 143, r1
    data_input = parse_input(open('./input.txt', 'r').read())
    [RULES, updates] = data_input
    r1 = part_1(updates)
    assert r1 == 5391, r1
    [RULES, updates] = test_input
    r2 = part_2(updates)
    assert r2 == 123, r2
    [RULES, updates] = data_input
    r2 = part_2(updates)
    assert r2 == 6142, r2
