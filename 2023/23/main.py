# https://adventofcode.com/2023/day/23
# --- Day 23: A Long Walk ---

import heapq
from collections import deque, defaultdict
from itertools import combinations

from helpers.utils import read_input_from_main

TEST_INPUT = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def part1(data):
    m = [[cell for cell in line] for line in data]
    start, end = (0, 1), (len(m) - 1, len(m[0]) - 2)

    longest_path_dist = 0
    queue = ([(0, (start, set()))])
    while queue:
        _, (coord, path) = heapq.heappop(queue)
        path = path | {coord}

        if coord == end:
            longest_path_dist = max(longest_path_dist, len(path))
            continue

        for d in DIRS:
            new_y, new_x = coord[0] + d[0], coord[1] + d[1]
            if 0 <= new_y < len(m) and 0 <= new_x < len(m[0]) and (new_y, new_x) not in path:
                if (next_step := m[new_y][new_x]) in '.<>^v':
                    if any([
                        next_step == '>' and d == (0, -1),
                        next_step == '<' and d == (0, 1),
                        next_step == '^' and d == (1, 0),
                        next_step == 'v' and d == (-1, 0)
                    ]):
                        # consider hitting a wall if moving in the opposite direction of the arrow
                        continue
                    # push the longest path to head
                    heapq.heappush(queue, (-len(path), ((new_y, new_x), path)))

    return longest_path_dist - 1 # minus the starting point

def part2(data):
    m = [[cell for cell in line] for line in data]
    start, end = (0, 1), (len(m) - 1, len(m[0]) - 2)

    # Transform the grid into a graph where each intersection is a graph node.
    # Each pair of connected nodes forms an edge with an associated distance.
    intersections = find_intersections(m, start, end)
    vertices_dist = compute_vertices(m, intersections)

    # Finally, find the longest path from start to end passing through all possible nodes.
    return find_longest_path(start, end, vertices_dist)


def find_intersections(m, start, end):
    size = len(m)-1
    intersections = [start, end]
    for y in range(0, size):
        for x in range(0, size):
            if m[y][x] == '.':
                neighbours = []
                for d in DIRS:
                    new_y, new_x = y + d[0], x + d[1]
                    if 0 <= new_y < len(m) and 0 <= new_x < len(m[0]) and m[new_y][new_x] in '^v<>':
                        neighbours.append((new_y, new_x))
                if len(neighbours) >= 3:
                    intersections.append((y, x))

    return intersections

def compute_vertices(m, intersections):
    # Find path between each intersection only if path exists
    vertices = {}
    for start, end in combinations(intersections, 2):
        queue = deque([(start, set())])
        while queue:
            coord, path = queue.pop()
            path = path | {coord}

            if coord in intersections and coord not in (end, start):
                continue
            if coord == end:
                vertices[(start, coord)] = len(path)
                continue

            for d in DIRS:
                new_y, new_x = coord[0] + d[0], coord[1] + d[1]
                if (
                    0 <= new_y < len(m) and 0 <= new_x < len(m[0])
                    and m[new_y][new_x] in '.^v<>'
                    and (new_y, new_x) not in path
                ):
                    queue.append(((new_y, new_x), path))

    return vertices

def find_longest_path(start, end, vertices_dist):
    # Precompute adjacency list for faster access
    adjacency = defaultdict(list)
    for vertice, dist in vertices_dist.items():
        a, b = tuple(vertice)
        adjacency[a].append((b, dist - 1))
        adjacency[b].append((a, dist - 1))

    longest_path_dist = 0

    def dfs(node, visited, dist):
        nonlocal longest_path_dist
        if node in visited:
            return
        if node == end:
            longest_path_dist = max(longest_path_dist, dist)
            return

        visited.add(node)
        for neighbor, edge_dist in adjacency[node]:
            if neighbor not in visited:
                dfs(neighbor, visited, dist + edge_dist)
        visited.remove(node)  # backtrack

    dfs(start, set(), 0)
    return longest_path_dist


if __name__ == "__main__":
    test_input = TEST_INPUT.splitlines()
    r1 = part1(test_input)
    assert r1 == 94, r1
    data = read_input_from_main(__file__)
    r1 = part1(data)
    assert r1 == 2206, r1
    print(f"#1: {r1}")
    r2 = part2(test_input)
    assert r2 == 154, r2
    r2 = part2(data)
    assert r2 == 6490, r2
    print(f"#2: {r2}")
