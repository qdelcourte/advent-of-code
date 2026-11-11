# https://adventofcode.com/2022/day/10
# --- Day 10: Cathode-Ray Tube ---

from helpers.utils import (
    read_input_from_main
)

TEST_INPUT = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""

def part1(instructions):
    x = 1
    cycle = 0
    signal_strengths = []

    for instruction in instructions:
        cycles = 1 if instruction == "noop" else 2

        for _ in range(cycles):
            cycle += 1
            if cycle in (20, 60, 100, 140, 180, 220):
                signal_strengths.append(cycle * x)

        if instruction.startswith("addx"):
            x += int(instruction.split()[1])

    return sum(signal_strengths)


def part2(instructions):
    x = 1
    pixels = []

    for instruction in instructions:
        cycles = 1 if instruction == "noop" else 2

        for _ in range(cycles):
            col = len(pixels) % 40
            pixels.append("#" if abs(col - x) <= 1 else ".")

        if instruction.startswith("addx"):
            x += int(instruction.split()[1])

    crt = [
        "".join(pixels[i:i + 40])
        for i in range(0, len(pixels), 40)
    ]
    print("\n".join(crt), end="\n\n")

if __name__ == "__main__":
    test_input = TEST_INPUT.splitlines()
    r1 = part1(test_input)
    assert r1 == 13140, r1
    data = read_input_from_main(__file__)
    r1 = part1(data)
    assert r1 == 15680, r1
    print(f"#1: {r1}")
    part2(test_input)
# ##..##..##..##..##..##..##..##..##..##..
# ###...###...###...###...###...###...###.
# ####....####....####....####....####....
# #####.....#####.....#####.....#####.....
# ######......######......######......####
# #######.......#######.......#######.....
    part2(data)
# ####.####.###..####.#..#..##..#..#.###..
# ...#.#....#..#.#....#..#.#..#.#..#.#..#.
# ..#..###..###..###..####.#....#..#.#..#.
# .#...#....#..#.#....#..#.#.##.#..#.###..
# #....#....#..#.#....#..#.#..#.#..#.#....
# ####.#....###..#....#..#..###..##..#....