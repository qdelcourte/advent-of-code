# https://adventofcode.com/2025/day/10
# --- Day 10: Factory ---

from scipy.optimize import linprog

from helpers.utils import (
	read_input_from_main
)

TEST_INPUT = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""

def part1(data):
    total_presses = 0
    for line in data:
        # Parse
        target_lights, buttons = line.split()[0][1:-1], line.split()[1:-1]
        bit_length = len(target_lights) - 1
        target_lights = int(target_lights.replace('.', '0').replace('#', '1'), 2)
        buttons = [sum(1 << (bit_length - int(i)) for i in b[1:-1].split(',')) for b in buttons]

        # Press any button until target and count how many iterations it takes
        # bitmask XOR(^) buttons to apply button's action
        button_presses, it = {0}, 0
        while target_lights not in button_presses:
            button_presses = set(c ^ b for b in buttons for c in button_presses)
            it += 1

        total_presses += it

    return total_presses


def part2(data):
    """
    The objective is to find the minimal solution which resolve :
        how many times each buttons need to be pushed to reach the target joltages
    Each of these coefficients is an unknown, so we tend to solve an equation with N unknown by minimizing.

    Mathematical approach with LP (Linear Programming) or Linear optimization;
    https://en.wikipedia.org/wiki/Linear_programming
    """

    total_presses = 0
    for line in data:
        buttons, target_joltages = line.split()[1:-1], list(map(int,line.split()[-1][1:-1].split(',')))

        # Minimize x0..xN : 1x0 + .. + 1xN <=> c = [1, .., 1] where N is the number of buttons
        # Coefficient is 1 because each button is different, then each button count as 1
        c = [1] * len(buttons)

        # such that A_eq matrice defines a constraint for each coefficient in c
        # note: first element of c is constrained by first elt of A_eq AND must be equal to first elt of b_eq.
        # in other words, A_eq specifies the coefficients of a linear equality constraint on ``x``
        # here we ignore useless button for element of target (b_eq) by constraining a coefficient of 0
        # ex: [[1, 1, 0], ...] means that the third doesn't impact first element of target, it can be ignored
        # <=> (1 * x0) + (1 * x1) + (0 * x2) = b_eq[0]
        a_eq = [[int(str(i) in b[1:-1].split(',')) for b in buttons] for i in range(len(target_joltages))]

        # b_eq; Each element of ``A_eq @ x``must equal the corresponding element of ``b_eq`` (A_eq and b_eq must have the same size)
        # integrality=1 -> Integer variable; decision variable must be an integer within bounds.

        # fun: is the optimal value of the objective function ``c @ x`` where ``x`` is the minimal solution vector.
        # Scalar product between ``c`` and ``x`` vectors: c⋅x = (c0 * x0) + ... + (cN * xN)
        total_presses += linprog(c=c, A_eq=a_eq, b_eq=target_joltages, integrality=1).fun

    return int(total_presses)


if __name__ == "__main__":
    test_input = TEST_INPUT.splitlines()
    r1 = part1(test_input)
    assert r1 == 7, r1
    data = read_input_from_main(__file__)
    r1 = part1(data)
    assert r1 == 491, r1
    print(f"#1: {r1}")
    r2 = part2(test_input)
    assert r2 == 33, r2
    r2 = part2(data)
    assert r2 == 20617, r2
    print(f"#2: {r2}")
