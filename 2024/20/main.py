# https://adventofcode.com/2024/day/20
# --- Day 20: Race Condition ---

import heapq
import numpy as np

TEST_INPUT = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""


def dijkstra(shape, start, end, obstacles) -> (int, list):
    queue, seen = [(0, start, [])], set()
    obstacles = set(obstacles)
    while queue:
        (cost, n, path) = heapq.heappop(queue)
        if n in seen:
            continue
        if n == end:
            return cost, path + [end]
        seen.add(n)
        path = path + [n]
        for d in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_position = (n[0] + d[0], n[1] + d[1])
            if node_position[0] >= shape[0] or node_position[0] < 0 or node_position[1] >= shape[1] or node_position[1] < 0:
                continue

            if node_position in obstacles:
                continue

            heapq.heappush(queue, (cost + 1, node_position, path))

    return None, None


def part_1(lines, target_save):
    # Get grid and remove borders
    m = np.array([list(line) for line in lines], str)[1:-1, 1:-1]

    start = tuple(map(int, list(zip(*np.where(m == 'S')))[0]))[::-1]
    end = tuple(map(int, list(zip(*np.where(m == 'E')))[0]))[::-1]
    obstacles = [obs[::-1] for obs in list(zip(*np.where(m == '#')))]

    base_cost, base_path = dijkstra(m.shape, start, end, obstacles)

    valid_cheats = set()
    for n in base_path:
        for d in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            obstacle_pos = (n[0] + d[0], n[1] + d[1])
            if obstacle_pos[0] >= m.shape[0] or obstacle_pos[0] < 0 or obstacle_pos[1] >= m.shape[1] or obstacle_pos[1] < 0:
                continue

            if m[obstacle_pos[::-1]] == '#' and obstacle_pos not in valid_cheats:
                node_position = (obstacle_pos[0] + d[0], obstacle_pos[1] + d[1])
                if m[node_position[::-1]] == '.':
                    if base_cost - (base_cost - abs(base_path.index(n) - base_path.index(node_position)) + 1) >= target_save:
                        valid_cheats.add(obstacle_pos)

    return len(valid_cheats)


def part_2(lines, target_save):
    # Get grid and remove borders
    m = np.array([list(line) for line in lines], str)[1:-1, 1:-1]

    start = tuple(map(int, list(zip(*np.where(m == 'S')))[0]))[::-1]
    end = tuple(map(int, list(zip(*np.where(m == 'E')))[0]))[::-1]
    obstacles = [obs[::-1] for obs in list(zip(*np.where(m == '#')))]

    base_cost, base_path = dijkstra(m.shape, start, end, obstacles)

    distance = 20
    checked = set()
    total_cheats = 0
    for c, cheat_start in enumerate(base_path):
        cheat_start_idx = base_path.index(cheat_start)
        for i in range(cheat_start[0]-distance, cheat_start[0]+distance+1):
            for j in range(cheat_start[1]-distance, cheat_start[1]+distance+1):
                if i >= m.shape[0] or i < 0 or j >= m.shape[1] or j < 0:
                    continue

                pair = frozenset((cheat_start, (i, j)))
                manhattan_dist = abs(cheat_start[0] - i) + abs(cheat_start[1] - j)
                if distance >= manhattan_dist >= 2 and m[*(i, j)[::-1]] in 'SE.' and pair not in checked:
                    checked.add(pair)
                    end_idx = base_path.index((i, j))
                    if base_cost - (cheat_start_idx + manhattan_dist + (base_cost - end_idx)) >= target_save:
                        total_cheats += 1
                    elif base_cost - (base_cost - cheat_start_idx + manhattan_dist + end_idx) >= target_save:
                        total_cheats += 1

    return total_cheats


if __name__ == '__main__':
    test_input = TEST_INPUT.splitlines()
    r1 = part_1(test_input, target_save=20)
    assert r1 == 5, r1
    data = open('./input.txt', 'r').read().splitlines()
    r1 = part_1(data, target_save=100)
    assert r1 == 1327, r1
    r2 = part_2(test_input, target_save=50)
    assert r2 == 285, r2
    r2 = part_2(data, target_save=100)
    assert r2 == 985737, r2
