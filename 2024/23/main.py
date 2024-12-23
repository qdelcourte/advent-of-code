# https://adventofcode.com/2024/day/23
# --- Day 23: LAN Party ---

from collections import defaultdict

TEST_INPUT = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""


def part_1(lines):
    connected = {tuple(sorted(line.split('-'))) for line in lines}

    groups = set()
    for c in connected:
        for t in connected:
            if (
                    c != t
                    and bool(len([1 for e in c+t if e.startswith('t')]))
                    and set(c) & set(t)
                    and tuple(sorted((set(c) ^ set(t)))) in connected
            ):
                new_group = tuple(sorted(set(set(c).union(set(t)))))
                groups.add(new_group)

    return len(groups)


def part_2(lines):
    connected = {tuple(sorted(line.split('-'))) for line in lines}

    # Gather all nodes neighbors
    nodes = defaultdict(set)
    for a, b in connected:
        nodes[a].add(b)
        nodes[b].add(a)

    def explore(n):
        seen.add(n)
        for next_node in nodes[n]:
            if next_node not in seen and all([next_node in nodes[s] for s in seen]):
                explore(next_node)

    # Explore each node and keep trace of the largest set
    m = None
    for node in nodes.keys():
        seen = set()
        explore(node)
        if m is None or len(seen) > len(m):
            m = seen.copy()

    return ','.join(sorted(m))


if __name__ == '__main__':
    test_input = TEST_INPUT.splitlines()
    r1 = part_1(test_input)
    assert r1 == 7, r1
    data = open('./input.txt', 'r').read().splitlines()
    r1 = part_1(data)
    assert r1 == 1062, r1
    r2 = part_2(test_input)
    assert r2 == 'co,de,ka,ta', r2
    r2 = part_2(data)
    assert r2 == 'bz,cs,fx,ms,oz,po,sy,uh,uv,vw,xu,zj,zm', r2
