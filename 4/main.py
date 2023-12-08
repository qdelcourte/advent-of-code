# https://adventofcode.com/2023/day/4
# --- Day 4: Scratchcards ---

import re

regex1 = re.compile(r'Card\s+(\d+):(.*)')


def part_1():
    result = 0
    for line in lines:
        winning_numbers, numbers = regex1.match(line).group(2).split('|')
        winning_numbers = list(filter(None, winning_numbers.split(' ')))
        numbers = list(filter(None, numbers.split(' ')))
        common = set(winning_numbers) & set(numbers)
        if len(common) == 0:
            continue
        result += int(2 ** (len(common) - 1))

    return result


def part_2():
    """
    Beurk
    """
    lines_copy = lines.copy()
    lines_length = len(lines_copy)
    cache = {}

    i = 0
    while i < lines_length:
        line = lines_copy[i]
        m = regex1.match(line)
        card_id = int(m.group(1))
        if card_id in cache:
            common = cache[card_id]
        else:
            winning_numbers, numbers = m.group(2).split('|')
            winning_numbers = list(filter(None, winning_numbers.split(' ')))
            numbers = list(filter(None, numbers.split(' ')))
            common = list(set(winning_numbers) & set(numbers))
            cache[card_id] = common
        i += 1
        if len(common) == 0:
            continue
        for id in range(card_id, card_id+len(common)):
            lines_copy.append(lines[id])
            lines_length += 1

    return len(lines_copy)


if __name__ == '__main__':
    lines = open('./input.txt', 'r').read().splitlines()
    r1 = part_1()
    assert r1 == 19855, r1
    print(f"#1: {r1}")
    r2 = part_2()
    assert r2 == 10378710, r2
    print(f"#2: {r2}")
