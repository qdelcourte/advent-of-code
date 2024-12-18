# https://adventofcode.com/2024/day/15
# --- Day 15: Warehouse Woes ---

import numpy as np

TEST_INPUT_1 = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

TEST_INPUT_2 = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""


TEST_INPUT_3 = """#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^"""


def pprint_matrix(m):
    for r in range(len(m)):  # rows
        for c in range(len(m[r])):  # columns
            print(m[r][c], " ", sep="", end="")
        print()
    print("-------------")


dirs = {
    '<': (0, -1),
    '>': (0, +1),
    '^': (-1, 0),
    'v': (+1, 0),
}


def parse(lines, wide=False):
    m = []
    origin_mouvements = []
    mouvements = []
    for line in lines:
        if 'v' in line:
            origin_mouvements.extend(list(line))
            mouvements.extend(list(map(lambda e: dirs[e], list(line))))
        elif '#' in line:
            if wide:
                m.append(list(line.replace('#', '##').replace('.', '..').replace('O', '[]').replace('@', '@.')))
            else:
                m.append(list(line))

    return np.array(m, str), mouvements


def part_1(lines):
    m, mouvements = parse(lines)
    robot_pos = tuple(map(int, list(zip(*np.where(m == '@')))[0]))
    m[robot_pos] = '.'

    boxes = set(list(zip(*np.where(m == 'O'))))

    for mouvement in mouvements:
        ry, rx = robot_pos
        dy, dx = mouvement
        next_pos = (ry + dy, rx + dx)
        tile = m[next_pos]
        if tile == '.':
            robot_pos = next_pos
        elif tile == 'O':
            next_pos_prime = next_pos
            while True:
                ny, nx = next_pos_prime
                next_pos_prime = (ny + dy, nx + dx)
                npy, npx = next_pos_prime
                if npy < 1 or npx < 1 or npy >= m.shape[0] or npx >= m.shape[1]:
                    break
                tile_prime = m[next_pos_prime]
                if tile_prime == '.':
                    boxes.remove(next_pos)
                    boxes.add(next_pos_prime)
                    m[next_pos_prime] = 'O'
                    m[next_pos] = '.'
                    robot_pos = next_pos
                    break
                elif tile_prime == '#':
                    break

    return sum(100 * y + x for y, x in boxes)


def dfs(m, tile1_pos, dir, boxes):
    if tile1_pos in boxes:
        return boxes
    if tile1_pos[0] < 1 or tile1_pos[1] < 1 or tile1_pos[0] >= m.shape[0] or tile1_pos[1] >= m.shape[1]:
        raise Exception

    tile1 = m[tile1_pos]

    if tile1 == '#':
        raise Exception
    if tile1 == '.':
        return boxes

    tile2_pos = (tile1_pos[0], tile1_pos[1] + (1 if tile1 == '[' else -1))

    boxes.append(tile1_pos)
    boxes.append(tile2_pos)

    dfs(m, (tile1_pos[0] + dir[0], tile1_pos[1] + dir[1]), dir, boxes)
    dfs(m, (tile2_pos[0] + dir[0], tile2_pos[1] + dir[1]), dir, boxes)

    return boxes


def part_2(lines):
    m, mouvements = parse(lines, wide=True)
    robot_pos = tuple(map(int, list(zip(*np.where(m == '@')))[0]))
    m[robot_pos] = '.'

    for it, mouvement in enumerate(mouvements):
        ry, rx = robot_pos
        dy, dx = mouvement
        next_pos = (ry + dy, rx + dx)
        tile = m[next_pos]
        if tile == '.':
            robot_pos = next_pos
        elif tile in '[]':
            first_tile_pos = next_pos
            try:
                b = dfs(m, first_tile_pos, mouvement, [])

                if abs(dy) == 1:
                    b = sorted(b, key=lambda x: x[0], reverse=dy == -1)
                elif abs(dx) == 1:
                    b = sorted(b, key=lambda x: x[1], reverse=dx == -1)

                to_move = {i: m[i] for i in b}

                for i in reversed(to_move.keys()):
                    m[i[0] + dy][i[1] + dx] = to_move[i]
                    m[i] = '.'

                robot_pos = next_pos
            except:
                pass

    boxes = set(list(zip(*np.where(m == '['))))

    return sum(100 * y + x for y, x in boxes)


if __name__ == '__main__':
    test_input_1 = TEST_INPUT_1.splitlines()
    t1 = part_1(test_input_1)
    assert t1 == 2028, t1
    test_input_2 = TEST_INPUT_2.splitlines()
    t2 = part_1(test_input_2)
    assert t2 == 10092, t2
    data = open('./input.txt', 'r').read().splitlines()
    r1 = part_1(data)
    assert r1 == 1465523, r1
    r2 = part_2(test_input_2)
    assert r2 == 9021, r2
    test_input_3 = TEST_INPUT_3.splitlines()
    r1 = part_2(test_input_3)
    assert r1 == 618, r1
    r2 = part_2(data)
    assert r2 == 1471049, r2
