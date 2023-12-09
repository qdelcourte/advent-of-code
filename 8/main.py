# https://adventofcode.com/2023/day/8
# --- Day 8: Haunted Wasteland ---

import re
from itertools import cycle
from math import lcm

regex1 = re.compile(r'(\w{3}) = \((\w{3}), (\w{3})\)')


def part_1():
    original_commands = list(map("LR".index, list(data[0])))
    tree = {key: (left, right) for key, left, right in map(lambda line: regex1.findall(line)[0], data[2:])}

    def search(commands, node):
        for c, cmd in enumerate(cycle(commands), start=1):
            if (node := tree[node][cmd]) == 'ZZZ':
                return c

    return search(original_commands.copy(), 'AAA')


def part_2():
    original_commands = list(map("LR".index, list(data[0])))
    tree = {key: (left, right) for key, left, right in map(lambda line: regex1.findall(line)[0], data[2:])}

    def search(commands, node):
        for c, cmd in enumerate(cycle(commands), start=1):
            if (node := tree[node][cmd])[-1] == 'Z':
                return c

    # Find the smallest positive integer that is divisible by both a and b
    # eg: 11A depth is 2 and 22A depth is 3
    #    => the smallest integer divisible by 2 and 3 is 6
    #    => 6 is the depth required by both to be equal
    # https://en.wikipedia.org/wiki/Least_common_multiple
    return lcm(*[
        search(original_commands.copy(), node)
        for node in list(filter(lambda x: x.endswith('A'), tree.keys()))
    ])


if __name__ == '__main__':
    data = open('./input.txt', 'r').read().splitlines()
    r1 = part_1()
    assert r1 == 12083, r1
    print(f"#1: {r1}")
    r2 = part_2()
    assert r2 == 13385272668829, r2
    print(f"#2: {r2}")

