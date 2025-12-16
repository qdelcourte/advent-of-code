# https://adventofcode.com/2025/day/11
# --- Day 11: Reactor ---

from collections import defaultdict
from copy import deepcopy

from helpers.utils import (
    read_input_from_main,
)

TEST_INPUT = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""

TEST_INPUT2 = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""

def find_paths(graph, src, dest):
    paths = []

    def dfs(path):
        current = path[-1]
        if current == dest:
            paths.append(path)
            return
        for adj in graph.get(current, []):
            dfs(path + [adj])

    dfs([src])
    return paths

def part1(data):
    neighbors = {s[0]: s[1].split(" ") for line in data if (s := line.split(": "))}

    return len(find_paths(neighbors, 'you', 'out'))


def indegree(edges):
    indegree_map = defaultdict(int)
    for _in, _out in edges:
        indegree_map.setdefault(_in, 0)
        indegree_map[_out] +=  1
    return indegree_map


def count_paths(graph, topo, start, end):
    distinct_paths = defaultdict(int)
    distinct_paths[start] = 1

    for u in topo:
        for v in graph[u]:
            distinct_paths[v] += distinct_paths[u]

    return distinct_paths[end]


def topo_sort(edges, neighbors):
    """
    L <- Empty list that will contain the sorted elements
    S <- Set of all nodes with no incoming edge

    while S is not empty do
        remove a node N from S
        add N to L
        for each node M with an edge E from N to M do
            remove edge E from the graph
            if M has no other incoming edges then
                insert M into S

    if graph has edges then
        return error  # graph has at least one cycle
    else
        return L  # a topologically sorted order
    """
    # https://networkx.org/nx-guides/content/algorithms/dag/index.html#kahn-s-algorithm
    # DG = nx.DiGraph(edges)
    # topo = list(nx.topological_sort(DG))

    edges = deepcopy(edges)

    # Empty list that will contain the sorted elements
    L = []

    # The node in_degree is the number of edges pointing to the node.
    indegree_map = indegree(edges)

    # Set of all nodes with no incoming edge
    S = [v for v, d in indegree(edges).items() if d == 0]

    while S:
        n = S.pop()
        L.append(n)
        for m in neighbors[n]:
            edges.remove((n, m))
            indegree_map[m] -= 1
            if indegree_map[m] == 0:
                S.append(m)
                del indegree_map[m]

    if edges: raise Exception('graph has at least one cycle')

    return L


def part2(data):
    edges = set()
    neighbors = {'out': []}
    for line in data:
        [out, expr] = line.split(": ")
        parts = expr.split(" ")
        neighbors[out] = parts
        edges.update(set((out, part) for part in parts))

    topo = topo_sort(edges, neighbors)

    svr_fft = count_paths(neighbors, topo, 'svr', 'fft')
    fft_dac = count_paths(neighbors, topo, 'fft', 'dac')
    dac_out = count_paths(neighbors, topo, 'dac', 'out')

    return svr_fft * fft_dac * dac_out


if __name__ == "__main__":
    test_input = TEST_INPUT.splitlines()
    r1 = part1(test_input)
    assert r1 == 5, r1
    data = read_input_from_main(__file__)
    r1 = part1(data)
    assert r1 == 552, r1
    print(f"#1: {r1}")
    test_input = TEST_INPUT2.splitlines()
    r2 = part2(test_input)
    assert r2 == 2, r2
    r2 = part2(data)
    assert r2 == 307608674109300, r2
    print(f"#2: {r2}")
