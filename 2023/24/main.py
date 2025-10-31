# https://adventofcode.com/2023/day/24
# --- Day 24: Never Tell Me The Odds ---

import re
from dataclasses import dataclass
from itertools import combinations

import numpy as np
from sympy import Symbol

from helpers.utils import (
    read_input_from_main
)

TEST_INPUT = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""

@dataclass
class Hailstone:
    x: int
    y: int
    z: int
    vx: int
    vy: int
    vz: int

    @property
    def position(self):
        return np.array((self.x, self.y, self.z))

    @property
    def velocity(self):
        return np.array((self.vx, self.vy, self.vz))



def parse(data):
    return (
        Hailstone(*map(int, re.fullmatch(r'(\d+),\s+(\d+),\s+(\d+)\s+@\s+(-?\d+),\s+(-?\d+),\s+(-?\d+)', line).groups()))
        for line in data
    )

def solve_linear2(a1, b1, c1, a2, b2, c2):
    """
    Solves a 2x2 linear system:
        a1*x + b1*y = c1
        a2*x + b2*y = c2

    Uses Cramer's rule to compute the unique solution.

    Returns
    -------
    tuple
        (x, y) solution of the system.
    """
    if (det := a1*b2 - a2*b1) == 0:
        return None
    return (c1*b2 - c2*b1) / det, (a1*c2 - a2*c1) / det


def part1(data, area):
    n = 0
    for a, b in combinations(parse(data), 2):
        """
            a.x + a.vx * t = b.x + b.vx * s 
        <=> a.vx * t - b.vx * s = b.x - a.x
        <=>    a1    -    b1    =    c1
        """
        r = solve_linear2(
            # a1, -b1, c1
            a.vx, -b.vx, b.x - a.x,
            # a2, -b2, c2
            a.vy, -b.vy, b.y - a.y
        )
        if r is None or any(n < 0 for n in r):
            continue

        x, y = a.x + a.vx * r[0], a.y + a.vy * r[0]
        if area[1] >= x >= area[0] and area[1] >= y >= area[0]:
            n += 1

    return n

def solve_three_collisions(h0: Hailstone, h1: Hailstone, h2: Hailstone):
    """
    Compute the initial position and velocity of a rock that collides with three hailstones.

    Parameters
    ----------
    h0, h1, h2 : Hailstone
        Three hailstones, each defined by a position (p) and velocity (v).

    Description
    -----------
    Each hailstone i is represented as (pᵢ, vᵢ).
    A collision between the rock (p₀, v₀) and hailstones h₁, h₂ occurs at times t₁, t₂:

        p₀ + t₁·v₀ = p₁ + t₁·v₁  ⇔  p₀ + t₁·v₀ = c₁
        p₀ + t₂·v₀ = p₂ + t₂·v₂  ⇔  p₀ + t₂·v₀ = c₂

    From the first equation: p₀ = c₁ - t₁·v₀
    Substitute into the second: (c₁ - t₁·v₀) + t₂·v₀ = c₂
    Simplify: c₁ - c₂ = v₀·(t₁ - t₂)
    Hence: v₀ = (c₁ - c₂) / (t₁ - t₂), and p₀ = c₁ - t₁·v₀

    To find t₁ and t₂, note that all collision points must be collinear:
        (p₁ + t₁·v₁) × (p₂ + t₂·v₂) = 0

    Expanding:
        (p₁ × p₂) + t₂·(p₁ × v₂) + t₁·(p₂ × v₁) + t₁·t₂·(v₁ × v₂) = 0

    Using the property (a×b)·a = (a×b)·b = 0, we can simplify by dotting both sides with v₂:
        (p₁ × p₂)·v₂ + t₁·[(p₂ × v₁)·v₂] = 0
        ⇒  t₁ = - ((p₁ × p₂)·v₂) / [(p₂ × v₁)·v₂]

    Similarly, by dotting with v₁:
        t₂ = - ((p₁ × p₂)·v₁) / [(p₁ × v₂)·v₁]

    Once t₁ and t₂ are known:
        c₁ = p₁ + t₁·v₁
        c₂ = p₂ + t₂·v₂
        v₀ = (c₁ - c₂) / (t₁ - t₂)
        p₀ = c₁ - t₁·v₀

    Returns
    -------
    dict
        {
            "t1": Collision time with hailstone 1,
            "t2": Collision time with hailstone 2,
            "c1": Collision point with hailstone 1,
            "c2": Collision point with hailstone 2,
            "v":  Computed velocity vector of the rock,
            "p":  Computed initial position vector of the rock
        }

    Notes
    -----
    This method assumes all hailstones and the rock move in 3D space with linear motion.
    It finds the unique rock trajectory intersecting the paths of h1 and h2 when measured
    relative to h0.
    """
    # relative positions and velocities to h0
    p1 = h1.position - h0.position
    p2 = h2.position - h0.position
    v1 = h1.velocity - h0.velocity
    v2 = h2.velocity - h0.velocity

    # compute cross/dot products and collision times
    c_p1_p2 = np.cross(p1, p2)
    t1 = (-np.dot(c_p1_p2, v2) / np.dot(np.cross(v1, p2), v2))
    t2 = (-np.dot(c_p1_p2, v1) / np.dot(np.cross(p1, v2), v1))

    # collision points
    c1 = h1.position + t1 * h1.velocity
    c2 = h2.position + t2 * h2.velocity

    # rock initial velocity and position
    # v = np.divide(np.subtract(c1, c2), (t1 - t2)).astype(int)
    v = ((c1 - c2) / (t1-t2)).astype(int)
    # p = np.subtract(c1, np.multiply(v, t1)).astype(int)
    p = c1 - t1 * v

    return {
        "t1": t1,
        "t2": t2,
        "c1": c1,
        "c2": c2,
        "v": v,
        "p": p,
    }

def solve_n_collisions(hailstones):
    """
    Transform solve_three_collisions to handle n hailstones.
    """
    h0 = hailstones.pop(0)

    # relative positions and velocities to h0
    rhailstones = [
        (h.position - h0.position, h.velocity - h0.velocity)
        for h in hailstones
    ]

    # TODO: May have a problem with this step
    # compute cross/dot products and collision times
    p1 = rhailstones[0][0]
    p2 = rhailstones[1][0]
    v1 = rhailstones[0][1]
    v2 = rhailstones[1][1]
    c_p1_p2 = np.cross(p1, p2)
    v_v1_p2 = np.cross(v1, p2)
    t = [
        (-np.dot(c_p1_p2, v2) / np.dot(v_v1_p2, v2)).astype(int)
    ] + [
        (-np.dot(np.cross(p1, p), v1) / np.dot(np.cross(p1, v), v1)).astype(int)
        for p, v in rhailstones[1:]
    ]

    # collision points
    c = [
        h.position + ti * h.velocity
        for h, ti in zip(hailstones, t)
    ]

    # TODO: fix this to handle n collisions properly
    # rock initial velocity and position
    # v = np.divide(np.subtract(c1, c2), (t1 - t2)).astype(int)
    # v = ((c1 - c2) / (t1-t2)).astype(int)
    # v = (reduce(lambda x, y: x - y, c)) / (reduce(lambda x, y: x - y, t))
    # p = np.subtract(c1, np.multiply(v, t1)).astype(int)
    # p = c[0] - t[0] * v

    for i, cp in enumerate(c[1:], start=1):
        # print(i, t[0], t[i])
        v = ((c[0] - cp) / (t[0] - t[i])).astype(int)
        p = (c[0] - t[0] * v).astype(int)
        if p.sum() == 983620716335751:
            print(c[0] - cp, t[0] - t[i], ((c[0] - cp) / (t[0] - t[i])).astype(int))
            print(p, p.sum() == 983620716335751)
        # print('v = ', v)

    p = (c[0] - t[0] * v).astype(int)

    return {
        "v": v,
        "p": p,
    }


def solve_equations(hailstones):
    """
    Solve the system of equations representing hailstone collisions.
    To know the initial position (x, y, z) and velocity (vx, vy, vz) of a rock that collides with multiple hailstones
    at times t0, t1, ..., tn, we set up the following equations for each hailstone i:
        x + ti * vx = hix + ti * hvix
        y + ti * vy = hiy + ti * hviy
        z + ti * vz = hiz + ti * hviz
    where (hix, hiy, hiz) is the initial position and (hvix, hviy, hviz) is the velocity of hailstone i.
    This leads to a system of linear equations that can be solved using sympy.
    """
    from sympy import solve, symbols as s
    from sympy.abc import x, y, z

    vx, vy, vz = s('vx vy vz')
    symbols = [vx, vy, vz, x, y, z]

    equations = []
    for i, h in enumerate(hailstones[:10]):
        ti = Symbol(f't{i}')
        symbols.append(ti)

        hpx, hpy, hpz = h.position
        hvx, hvy, hvz = h.velocity
        equations.extend((
            x + ti * vx - (hpx + ti * hvx),
            y + ti * vy - (hpy + ti * hvy),
            z + ti * vz - (hpz + ti * hvz),
        ))

    solutions = solve(equations, *symbols, dict=True)

    return sum(solutions[0][var] for var in (x, y, z))


def part2(data):
    hailstones = list(parse(data))

    # This one works with test input, but not with the full input
    print('3 collisions', solve_three_collisions(hailstones[0], hailstones[1], hailstones[2])['p'].sum())

    # This one works with test input, but not with the full input
    print('N collisions', solve_n_collisions(hailstones)['p'].sum())

    return solve_equations(hailstones)


if __name__ == "__main__":
    test_input = TEST_INPUT.splitlines()
    r1 = part1(test_input, (7, 27))
    assert r1 == 2, r1
    data = read_input_from_main(__file__)
    r1 = part1(data, (200000000000000, 400000000000000))
    assert r1 == 11995, r1
    print(f"#1: {r1}")
    r2 = part2(test_input)
    assert r2 == 47, r2
    r2 = part2(data)
    assert r2 == 983620716335751, r2
    print(f"#2: {r2}")
