# https://adventofcode.com/2024/day/13
# --- Day 13: Claw Contraption ---

import re

TEST_INPUT = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""


def parse(lines, part2=False):
    machines = []
    machine = {}

    for line in lines + ['']:
        if line == '':
            if machine:
                machines.append(machine)
                machine = {}
            continue

        label, x, y = re.match(r"(Button [AB]|Prize): X[+=](\d+), Y[+=](\d+)", line).groups()
        x, y = int(x), int(y)

        if label == "Button A":
            machine['A'] = (x, y)
        elif label == "Button B":
            machine['B'] = (x, y)
        elif label == "Prize":
            machine['prize'] = (x + (10**13 if part2 else 0), y + (10**13 if part2 else 0))

    return machines


def get_solution(eq1, eq2):
    # Définir les coefficients des équations
    a1, b1, c1 = eq1
    a2, b2, c2 = eq2

    # Calculer le déterminant
    if (det := a1 * b2 - a2 * b1) != 0:
        x = (c1 * b2 - c2 * b1) / det
        y = (a1 * c2 - a2 * c1) / det
        if x.is_integer() and y.is_integer():
            return x, y


def tokens(a, b):
    return a * 3 + b


def solve(lines, part2=False):
    return sum(tokens(*s) for machine in parse(lines, part2) if
               (s := get_solution((machine['A'][0], machine['B'][0], machine['prize'][0]),
                                  (machine['A'][1], machine['B'][1], machine['prize'][1]))))


if __name__ == '__main__':
    test_input = TEST_INPUT.splitlines()
    r1 = solve(test_input)
    assert r1 == 480, r1
    data = open('./input.txt', 'r').read().splitlines()
    r1 = solve(data)
    assert r1 == 32067, r1
    r2 = solve(data, part2=True)
    assert r2 == 92871736253789, r2
