# https://adventofcode.com/2024/day/18
# --- Day 18: RAM Run ---

import heapq

TEST_INPUT = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""


def dijkstra(shape, obstacles):
    start, end = (0, 0), (shape[0], shape[1])
    queue, seen = [(0, start, [])], set()
    obstacles = set(obstacles)
    while queue:
        (cost, n, path) = heapq.heappop(queue)
        if n in seen:
            continue
        if n == end:
            return cost
        seen.add(n)
        path = path + [n]
        for d in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_position = (n[0] + d[0], n[1] + d[1])
            if node_position[0] > shape[0] or node_position[0] < 0 or node_position[1] > shape[1] or node_position[1] < 0:
                continue

            if node_position in obstacles:
                continue

            heapq.heappush(queue, (cost + 1, node_position, path))

    return None


def part_1(lines, shape, k):
    corrupted = list(map(lambda x: (int(x.split(',')[0]), int(x.split(',')[1])), lines))[:k]
    return dijkstra(shape, corrupted)


def part_2(lines, shape):
    corrupted = list(map(lambda x: (int(x.split(',')[0]), int(x.split(',')[1])), lines))

    for i in reversed(range(1, len(corrupted)+1)):
        if dijkstra(shape, corrupted[:i]) is not None:
            return ','.join(map(str, corrupted[i]))


if __name__ == '__main__':
    test_input = TEST_INPUT.splitlines()
    r1 = part_1(test_input, (6, 6), 12)
    assert r1 == 22, r1
    data = open('./input.txt', 'r').read().splitlines()
    r1 = part_1(data, (70, 70), 1024)
    assert r1 == 344, r1
    r2 = part_2(test_input, (6, 6))
    assert r2 == '6,1', r2
    r2 = part_2(data, (70, 70))
    assert r2 == '46,18', r2
