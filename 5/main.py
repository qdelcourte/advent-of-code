# https://adventofcode.com/2022/day/5
# --- Day 5: Supply Stacks ---

from collections import defaultdict


TEST_INPUT = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""


def parse(lines):
    split_index = lines.index("")
    stack_lines = lines[:split_index]
    instructions = [
        (int(parts[1]), int(parts[3]), int(parts[5]))
        for parts in (line.split() for line in lines[split_index + 1:])
    ]

    stacks = defaultdict(list)
    column_indices = {idx: int(num) for idx, num in enumerate(stack_lines[-1].split())}

    for line in reversed(stack_lines[:-1]):
        for pos, col_num in column_indices.items():
            char_index = pos * 4 + 1
            if char_index < len(line) and line[char_index].isalpha():
                stacks[col_num].append(line[char_index])
    
    return stacks, instructions


def solve(lines, part2=False):
    stacks, instructions = parse(lines)

    for count, from_stack, to_stack in instructions:
        to_move = stacks[from_stack][-count:]
        stacks[to_stack].extend(to_move if part2 else reversed(to_move))
        stacks[from_stack] = stacks[from_stack][:-count]

    return ''.join(stack[-1] for stack in stacks.values())


if __name__  == '__main__':
    test_input = TEST_INPUT.splitlines()
    r1 = solve(test_input)
    assert r1 == 'CMZ', r1
    data = open('./input.txt').read().splitlines()
    r1 = solve(data)
    assert r1 == 'TQRFCBSJJ', r1
    r2 = solve(test_input, part2=True)
    assert r2 == 'MCD', r2
    r2 = solve(data, part2=True)
    assert r2 == 'RMHFJNVFP', r2
