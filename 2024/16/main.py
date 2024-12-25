# https://adventofcode.com/2024/day/16
# --- Day 16: Reindeer Maze ---

import heapq
import numpy as np

TEST_INPUT_1 = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

TEST_INPUT_2 = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""


TEST_INPUT_3 = """##########
#.......E#
#.##.#####
#..#.....#
##.#####.#
#S.......#
##########"""


class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None, dir=None):
        self.parent = parent
        self.position = position
        self.dir = dir  # direction

        self.score = 0

    def __str__(self):
        return f"score: {self.score}, ({self.position[0]}, {self.position[1]})"

    def __eq__(self, other):
        return self.score == other.score

    def __lt__(self, other):
        return self.score < other.score

    def __gt__(self, other):
        return self.score > other.score


def astar(m, part2=False) -> list:
    end_pos = tuple(map(int, list(zip(*np.where(m == 'E')))[0]))
    start_pos = tuple(map(int, list(zip(*np.where(m == 'S')))[0]))

    start_node = Node(None, (start_pos[1], start_pos[0]), (1, 0))
    end_node = Node(None, (end_pos[1], end_pos[0]))

    queue = [start_node]
    visited = {}
    paths = []

    # Loop until you find the end
    while queue:
        current_node = heapq.heappop(queue)
        visited[(current_node.position, current_node.dir)] = True

        # Found the goal
        if current_node.position == end_node.position:
            path = []
            current = current_node
            while current is not None:
                path.append(current)
                current = current.parent
            if part2:
                new_path = path[::-1]
                if paths:
                    if paths[0][-1].score > new_path[-1].score:
                        paths = [new_path]
                    elif paths[0][-1].score == new_path[-1].score:
                        paths.append(new_path)
                else:
                    paths.append(new_path)
                continue
            else:
                return path[::-1]  # Return reversed path

        # Generate children
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares
            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > m.shape[1] or node_position[0] < 0 or node_position[1] > m.shape[0] or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if m[node_position[1]][node_position[0]] == '#':
                continue

            child = Node(current_node, node_position, new_position)
            if (child.position, child.dir) in visited:
                continue

            child.score = current_node.score + (1001 if current_node.dir != child.dir else 1)

            heapq.heappush(queue, child)

    return paths


def part_1(lines):
    m = np.array([list(line) for line in lines], str)

    return astar(m)[-1].score


def part_2(lines):
    m = np.array([list(line) for line in lines], str)

    nodes = []
    for path in astar(m, part2=True):
        nodes.extend(list(map(lambda n: n.position, path)))

    return len(set(nodes))


if __name__ == '__main__':
    test_input_1 = TEST_INPUT_1.splitlines()
    t1 = part_1(test_input_1)
    assert t1 == 7036, t1
    test_input_2 = TEST_INPUT_2.splitlines()
    t2 = part_1(test_input_2)
    assert t2 == 11048, t2
    test_input_3 = TEST_INPUT_3.splitlines()
    t3 = part_1(test_input_3)
    assert t3 == 4013, t3
    data = open('./input.txt', 'r').read().splitlines()
    r1 = part_1(data)
    assert r1 == 102504, r1
    t1 = part_2(test_input_1)
    assert t1 == 45, t1
    t2 = part_2(test_input_2)
    assert t2 == 64, t2
    r2 = part_2(data)
    assert r2 == 535, r2
