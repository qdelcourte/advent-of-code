# https://adventofcode.com/2024/day/17
# --- Day 17: Chronospatial Computer ---

from copy import deepcopy

TEST_INPUT = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""

TEST_INPUT_2 = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""


def parse(lines):
    computer = {}
    for line in lines + ['']:
        if 'Register' in line:
            [_, var, value] = line.split()
            computer[var[0]] = int(value)
        elif 'Program' in line:
            [_, program] = line.split()
            computer['program'] = list(map(int, program.split(',')))
    return computer


def test_op():
    default_computer = {'A': 0, 'B': 0, 'C': 0, 'program': [], 'output': []}

    # If register C contains 9, the program 2,6 would set register B to 1.
    computer = deepcopy(default_computer)
    computer['C'] = 9
    computer['program'] = [2, 6]
    computer = run(computer)
    assert computer['B'] == 1

    # If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
    computer = deepcopy(default_computer)
    computer['A'] = 10
    computer['program'] = [5, 0, 5, 1, 5, 4]
    computer = run(computer)
    assert computer['output'] == [0, 1, 2]

    # If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
    computer = deepcopy(default_computer)
    computer['A'] = 2024
    computer['program'] = [0, 1, 5, 4, 3, 0]
    computer = run(computer)
    assert computer['A'] == 0
    assert computer['output'] == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0], computer

    # If register B contains 29, the program 1,7 would set register B to 26.
    computer = deepcopy(default_computer)
    computer['B'] = 29
    computer['program'] = [1, 7]
    computer = run(computer)
    assert computer['B'] == 26

    # If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354.
    computer = deepcopy(default_computer)
    computer['B'] = 2024
    computer['C'] = 43690
    computer['program'] = [4, 0]
    computer = run(computer)
    assert computer['B'] == 44354


def run(computer):
    a, b, c, program = computer['A'], computer['B'], computer['C'], computer['program']
    nb_instructions = len(program)
    output = []
    pointer = 0
    while pointer < nb_instructions:
        [opcode, operand] = program[pointer:pointer + 2]
        combo = {0: 0, 1: 1, 2: 2, 3: 3, 4: a, 5: b, 6: c, 7: 7}

        match opcode:
            case 0: a = a // 2 ** combo[operand]  # adv
            case 1: b = b ^ operand  # bxl
            case 2: b = combo[operand] % 8  # bst
            case 3: pointer = operand - 2 if a else pointer  # jnz
            case 4: b = b ^ c  # bxc
            case 5: output.append(combo[operand] % 8)  # out
            case 6: b = a // 2 ** combo[operand]  # bdv
            case 7: c = a // 2 ** combo[operand]  # cdv

        pointer += 2

    return {
        'output': output,
        'A': a,
        'B': b,
        'C': c
    }


def part_1(lines):
    computer = parse(lines)
    output = run(computer)
    return ','.join(map(str, output['output']))


def part_2(lines):
    computer = parse(lines)
    program = computer['program']

    candidates = [0]
    for digit in range(1, len(program) + 1):
        out = []

        for candidate in candidates:
            for offset in range(8):
                a = 8 * candidate + offset
                computer['A'] = a

                if run(computer)['output'] == program[-digit:]:
                    out.append(a)

        candidates = out

    return min(candidates)


if __name__ == '__main__':
    test_op()
    test_input = TEST_INPUT.splitlines()
    r1 = part_1(test_input)
    assert r1 == '4,6,3,5,6,3,5,2,1,0', r1
    data = open('./input.txt', 'r').read().splitlines()
    r1 = part_1(data)
    assert r1 == '7,3,0,5,7,1,4,0,5', r1
    test_input_2 = TEST_INPUT_2.splitlines()
    r2 = part_2(test_input_2)
    assert r2 == 117440, r2
    r2 = part_2(data)
    assert r2 == 202972175280682, r2
