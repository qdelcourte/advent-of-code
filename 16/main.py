# https://adventofcode.com/2023/day/16
# --- Day 16: The Floor Will Be Lava ---

TEST_INPUT = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""


def print_energized(originals, energized):
    energized_lines = originals.copy()
    for _x, _y in energized:
        energized_lines[_y] = energized_lines[_y][:_x] + "#" + energized_lines[_y][_x + 1:]
    print('\n'.join(energized_lines))


def beam_pathfinding(lines, _from=None, _to=None, print_result=False):
    # Start from top-left corner to the right by default
    beams = [(_from or (-1, 0), _to or (0, 0))]
    beams_checked = set()
    energized = set()

    while beams:
        prev, curr = beams.pop()
        beams_checked.add((prev, curr))
        x, y = curr

        try:
            tile = lines[y][x]
            if y < 0 or x < 0:
                raise IndexError
        except IndexError:
            continue

        energized.add((x, y))
        x_prev, y_prev = prev
        x_dir = x - x_prev
        y_dir = y - y_prev

        next_beams = []
        if tile == '\\':
            next_beams.append((curr, (x + y_dir, y + x_dir)))
        elif tile == "/":
            next_beams.append((curr, (x - y_dir, y - x_dir)))
        elif tile == ".":
            next_beams.append((curr, (x + x_dir, y + y_dir)))
        elif tile == '-':
            if abs(x_dir) == 1:
                next_beams.append((curr, (x + x_dir, y)))
            else:
                next_beams.append((curr, (x - y_dir, y)))
                next_beams.append((curr, (x + y_dir, y)))
        elif tile == "|":
            if abs(x_dir) == 1:
                next_beams.append((curr, (x, y - x_dir)))
                next_beams.append((curr, (x, y + x_dir)))
            else:
                next_beams.append((curr, (x, y + y_dir)))
        for next_beam in next_beams:
            if next_beam not in beams_checked:
                beams.append(next_beam)

    if print_result:
        print_energized(lines, energized)

    return len(energized)


def test_1():
    return beam_pathfinding(TEST_INPUT.splitlines())


def part_1():
    return beam_pathfinding(lines)


def best_path(lines):
    line_len = len(lines[0])
    nb_lines = len(lines)

    configurations = []
    for i in range(len(lines)):
        configurations.append(((-1, i), (0, i)))
        configurations.append(((line_len, i), (line_len-1, i)))
    for i in range(line_len):
        configurations.append(((i, -1), (i, 0)))
        configurations.append(((i, nb_lines), (i, nb_lines-1)))

    return max([beam_pathfinding(lines, *config) for config in configurations])


def test_2():
    return best_path(TEST_INPUT.splitlines())


def part_2():
    return best_path(lines)


if __name__ == '__main__':
    t1 = test_1()
    assert t1 == 46, t1
    print(f"test 1: {t1}")
    lines = open('./input.txt', 'r').read().splitlines()
    r1 = part_1()
    assert r1 == 8323, r1
    print(f"#1: {r1}")
    t2 = test_2()
    assert t2 == 51, t2
    print(f"test 2: {t2}")
    r2 = part_2()
    assert r2 == 8491, r2
    print(f"#2: {r2}")
