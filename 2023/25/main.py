# https://adventofcode.com/2023/day/25
# --- Day 25: Snowverload ---

from collections import deque

import networkx as nx

from helpers.utils import (
    read_input_from_main
)

TEST_INPUT = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""

def graph_connected_components(graph):
    """
    Find connected components in an undirected graph.
    https://en.wikipedia.org/wiki/Component_(graph_theory)
    """
    visited = set()
    components = []
    for node in graph:
        if node in visited:
            continue
        visited.add(node)
        queue = deque([node])
        component = set()
        while queue:
            current = queue.popleft()
            component.add(current)
            for neigh in graph[current]:
                if neigh not in visited:
                    visited.add(neigh)
                    queue.append(neigh)

        components.append(component)

    return components


def part1(data, test=False):
    mapping = set()
    for line in data:
        [out, expr] = line.split(": ")
        parts = expr.split(" ")
        for part in parts:
            if (out, part) not in mapping and (part, out) not in mapping:
                mapping.add((part, out))

    # Generate graph visualization to detect articulation points by hand...
    # g = graphviz.Graph(filename=read_from_main(__file__, "graph"), format='png', engine='fdp')
    # g.edges(mapping)
    # g.render(view=True)
    #
    # if test:
    #     # jqt/nvd bvb/cmg pzl/hfx
    #     mapping.remove(('nvd', 'jqt'))
    #     mapping.remove(('bvb', 'cmg'))
    #     mapping.remove(('hfx', 'pzl'))
    # else:
    #     # cbl/vmq nvf/bvz xgz/klk
    #     mapping.remove(('vmq', 'cbl'))
    #     mapping.remove(('nvf', 'bvz'))
    #     mapping.remove(('xgz', 'klk'))
    #
    # # Build graph
    # graph = {}
    # for a, b in mapping:
    #     graph.setdefault(a, set()).add(b)
    #     graph.setdefault(b, set()).add(a)
    #
    # components = graph_connected_components(graph)
    # assert len(components) == 2, components
    # return len(components[0]) * len(components[1])

    # Automate minimum cut detection
    # https://research.google/blog/solving-the-minimum-cut-problem-for-undirected-graphs/
    # https://en.wikipedia.org/wiki/Stoer%E2%80%93Wagner_algorithm
    G = nx.Graph()
    G.add_edges_from(mapping)
    cut_value, partition = nx.stoer_wagner(G)
    S, T = partition

    assert len(partition) == 2, partition
    return len(S) * len(T)


if __name__ == "__main__":
    test_input = TEST_INPUT.splitlines()
    r1 = part1(test_input, test=True)
    assert r1 == 54, r1
    data = read_input_from_main(__file__)
    r1 = part1(data)
    assert r1 == 583632, r1
