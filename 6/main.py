# https://adventofcode.com/2023/day/6
# --- Day 6: Wait For It ---

import re
from functools import reduce
from math import sqrt, ceil
from operator import mul


# Find solutions for x, where x is the time accorded to do the distance D in a time total of T
# initial speed is time elapsed and as long as v = x
# (T - x) x v = (T - x) * x = Tx - x^2
# Inequality is: x^2 - Tx >= D
# So search solutions for: x^2 - Tx - D >= 0 <=> (x - sqrt(D)) * (x + sqrt(D)) >= 0

def solve_inequality(t, d):
    delta = t**2 - 4*d
    root1 = (-t + sqrt(delta)) / 2
    root2 = (-t - sqrt(delta)) / 2
    [start, end] = [ceil(abs(root1) + int(root1.is_integer())), int(abs(root2) - int(root2.is_integer()))]
    return end - start + 1


def solve(transform: callable = lambda x: x):
    [times, distances] = data
    times = map(int, re.findall(r'\d+', transform(times)))
    distances = map(int, re.findall(r'\d+', transform(distances)))
    race_solutions = [solve_inequality(t, d) for t, d in list(zip(times, distances))]
    return reduce(mul, race_solutions)


def part_1():
    return solve()


def part_2():
    return solve(lambda x: x.replace(' ', ''))


if __name__ == '__main__':
    data = open('./input.txt', 'r').read().splitlines()
    r1 = part_1()
    assert r1 == 293046, r1
    print(f"#1: {r1}")
    r2 = part_2()
    assert r2 == 35150181, r2
    print(f"#2: {r2}")
