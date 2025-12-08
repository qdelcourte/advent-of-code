# https://adventofcode.com/2025/day/8
# --- Day 8: Playground ---
import heapq
import math
from dataclasses import dataclass
from itertools import combinations

from helpers.utils import (
	read_input_from_main
)

TEST_INPUT = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""

@dataclass
class Box(list):
    x: int
    y: int
    z: int

    def __hash__(self):
        return hash(tuple([self.x, self.y, self.z]))

    @staticmethod
    def dist(a: 'Box', b: 'Box'):
        return math.dist([a.x, a.y, a.z], [b.x, b.y, b.z])

def parse(data): return [Box(*map(int, line.split(','))) for line in data]

def boxes_pair_by_dist(boxes):
    return dict(heapq.nsmallest(
        10000,
        (((a, b), Box.dist(a, b)) for a, b in combinations(boxes, 2)),
        key=lambda x: x[1]
    ))

def _merge_pair(a: Box, b: Box, circuits_references):
    circuit_a = circuits_references.get(a)
    circuit_b = circuits_references.get(b)
    if circuit_a and circuit_b and circuit_a == circuit_b:
        return circuits_references
    if circuit_a and circuit_b:
        circuit = circuit_a | circuit_b
    elif circuit_a:
        circuit = circuit_a | {b}
    elif circuit_b:
        circuit = circuit_b | {a}
    else:
        circuit = {a, b}
    for k in circuit:
        circuits_references[k] = circuit
    return circuits_references

def part1(data, remaining_connections = 10):
    circuits_references = {}
    for a, b in boxes_pair_by_dist(parse(data)):
        if remaining_connections == 0: break
        circuits_references = _merge_pair(a, b, circuits_references)
        remaining_connections -= 1

    unique_circuits = {frozenset(c) for c in circuits_references.values()}
    circuits_by_len = sorted((len(c) for c in unique_circuits), reverse=True)

    return math.prod(circuits_by_len[:3])

def part2(data):
    boxes = parse(data)
    n = len(boxes)
    circuits_references = {}
    last_two = None
    for a, b in boxes_pair_by_dist(boxes):
        circuits_references = _merge_pair(a, b, circuits_references)
        if n == len(circuits_references.get(a, [])):
            last_two = (a, b)
            break

    return last_two[0].x * last_two[1].x


if __name__ == "__main__":
    test_input = TEST_INPUT.splitlines()
    r1 = part1(test_input, remaining_connections=10)
    assert r1 == 40, r1
    data = read_input_from_main(__file__)
    r1 = part1(data, remaining_connections=1000)
    assert r1 == 62186, r1
    print(f"#1: {r1}")
    r2 = part2(test_input)
    assert r2 == 25272, r2
    r2 = part2(data)
    assert r2 == 8420405530, r2
    print(f"#2: {r2}")
