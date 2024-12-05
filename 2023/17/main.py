# https://adventofcode.com/2023/day/17
# --- Day 17: Clumsy Crucible ---

import heapq
import math
from collections import defaultdict

TEST_INPUT = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""


def dijkstra(grid, is_direction_valid):
    start = (0, 0)
    n, m = len(grid), len(grid[0])
    goal = (n - 1, m - 1)

    prev_point = {}
    heat_map = defaultdict(lambda: math.inf)
    # (cost, node(x,y), last_direction, steps)
    queue = [(0, start, (0, 0), 0)]

    while queue:
        cost, (curr_x, curr_y), (d_x, d_y), steps = heapq.heappop(queue)
        last_direction = (d_x, d_y)
        if (curr_x, curr_y) == goal:
            return cost, prev_point, last_direction, steps

        for next_d_x, next_d_y in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            next_x, next_y = curr_x + next_d_x, curr_y + next_d_y
            next_d = (next_d_x, next_d_y)
            new_steps = is_direction_valid(last_direction, next_d_x, next_d_y, steps)
            if new_steps is None:
                continue

            if n > next_y >= 0 and m > next_x >= 0:
                new_cost = cost + int(grid[next_y][next_x])
                if new_cost < heat_map[(next_x, next_y, next_d, new_steps)]:
                    heat_map[(next_x, next_y, next_d, new_steps)] = new_cost
                    prev_point[(next_x, next_y, next_d, new_steps)] = (curr_x, curr_y, last_direction, steps)
                    heapq.heappush(queue, (new_cost, (next_x, next_y), (next_d_x, next_d_y), new_steps))


def find_shortest_path(prev_point_graph, end_point):
    shortest_path = []
    current_point = end_point
    while current_point is not None:
        shortest_path.append(current_point)
        current_point = prev_point_graph.get(current_point, None)
    shortest_path.reverse()
    return shortest_path


def print_map(grid, prev_point, end_point, last_direction, steps):
    path = find_shortest_path(prev_point, (end_point[0], end_point[1], last_direction, steps))
    f = grid.copy()
    for x, y, _, _ in path:
        f[y][x] = '.'

    for i, k in enumerate(f):
        f[i] = ''.join(map(str, f[i]))
    print('\n'.join(f))


def part_1(data):
    def is_direction_valid(last_direction, new_dx, new_dy, steps):
        if last_direction == (-new_dx, -new_dy):
            return None
        elif last_direction != (new_dx, new_dy):
            return 1
        elif last_direction == (new_dx, new_dy):
            steps += 1
            if steps <= 3:
                return steps

    r, prev_point, last_direction, steps = dijkstra(data, is_direction_valid)
    # print_map(data, prev_point, (len(data)-1, len(data[0])-1), last_direction, steps)

    return r


def part_2(data):
    def is_direction_valid(last_direction, new_dx, new_dy, steps):
        if last_direction == (new_dx, new_dy):
            steps += 1
            if steps <= 10:
                return steps
        elif last_direction == (-new_dx, -new_dy):
            return None
        elif last_direction != (new_dx, new_dy):
            if steps < 4 and last_direction != (0, 0):
                return None
            return 1

    r, _, _, _ = dijkstra(data, is_direction_valid)

    return r


if __name__ == '__main__':
    t1 = part_1(list(map(lambda l: list(map(int, list(l))), TEST_INPUT.splitlines())))
    assert t1 == 102, t1
    print(f"test 1: {t1}")
    data = open('./input.txt', 'r').read().splitlines()
    r1 = part_1(list(map(lambda l: list(map(int, list(l))), data)))
    assert r1 == 785, r1
    print(f"#1: {r1}")
    t2 = part_2(list(map(lambda l: list(map(int, list(l))), TEST_INPUT.splitlines())))
    assert t2 == 94, t2
    print(f"test 2: {t2}")
    r2 = part_2(list(map(lambda l: list(map(int, list(l))), data)))
    assert r2 == 922, r2
    print(f"#2: {r2}")
