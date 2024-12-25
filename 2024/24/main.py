# https://adventofcode.com/2024/day/24
# --- Day 24: Crossed Wires ---

from collections import deque
from itertools import batched
import graphviz

TEST_INPUT = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""


def parse(lines):
    inputs = {}
    operations = []
    for line in lines:
        if ':' in line:
            [inp, v] = line.split(': ')
            inputs[inp] = int(v)
        elif '->' in line:
            [op1, op, op2, _, to] = line.split()
            operations.append((op1, op, op2, to))

    return inputs, operations


def to_binary(inputs, i):
    inp = {k: v for k, v in inputs.items() if k.startswith(i)}
    return ''.join(str(inp[k]) for k in sorted(inp.keys(), key=lambda k: -int(k[1:])))


def to_decimal(inputs, i):
    return int(to_binary(inputs, i), 2)


def run(inputs, operations):
    queue = deque(operations)
    while queue:
        op1, op, op2, to = queue.popleft()
        if op1 in inputs and op2 in inputs:
            match op:
                case 'AND': inputs[to] = inputs[op1] and inputs[op2]
                case 'OR':  inputs[to] = inputs[op1] or inputs[op2]
                case 'XOR': inputs[to] = inputs[op1] ^ inputs[op2]
        else:
            queue.append((op1, op, op2, to))

    return to_decimal(inputs, 'z'), to_binary(inputs, 'z')


def part_1(lines):
    return run(*parse(lines))[0]


def part_2(lines):
    # Create mapping of ends node operation
    inputs, operations = parse(lines)
    mapping = {to: (op1, op2, op) for op1, op, op2, to in operations}

    # Search x + y = z
    #  111100101001000011100011110010101111011001101
    # +110001010011000010001101100110010100000011001
    # ----------------------------------------------
    # 1101101111100000101110001011001000011011100110

    # 33338013867725 + 27101540591641
    # Expected: 1101101111100000101110001011001000011011100110
    # Actual:   1101110011100000101101101011000111111100000110
    expected = '1101101111100000101110001011001000011011100110'

    # Visualize operations executions and dependencies
    # and try to find anomalies, wrong patterns,...
    # g = graphviz.Digraph(filename="graph.gv", format='png', engine='fdp')
    # colors = {'AND': 'green', 'OR': 'blue', 'XOR': 'red'}
    # for n in sorted(mapping.keys()):
    #     if n.startswith('z'):
    #         g.node(n, shape='star')
    #     g.edge(mapping[n][0], n, color=colors[mapping[n][2]])
    #     g.edge(mapping[n][1], n, color=colors[mapping[n][2]])
    # g.render(view=True)

    # Wires to switch according to the manual debugging from the previous step
    to_try = ['frt', 'z23', 'sps', 'z11', 'tst', 'z05', 'cgh', 'pmd']

    # Switch wires
    new_operations = mapping.copy()
    for a, b in batched(to_try, n=2):
        new_operations[a] = mapping[b]
        new_operations[b] = mapping[a]

    # Run the new configuration and check the result
    new_operations = [(op1, op, op2, to) for to, (op1, op2, op) in new_operations.items()]
    if run(inputs, new_operations)[1] == expected:
        return ','.join(sorted(to_try))


if __name__ == '__main__':
    test_input = TEST_INPUT.splitlines()
    r1 = part_1(test_input)
    assert r1 == 2024, r1
    data = open('./input.txt', 'r').read().splitlines()
    r1 = part_1(data)
    assert r1 == 60714423975686, r1
    r2 = part_2(data)
    assert r2 == 'cgh,frt,pmd,sps,tst,z05,z11,z23', r2
