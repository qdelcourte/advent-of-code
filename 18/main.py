# https://adventofcode.com/2023/day/18
# --- Day 18: Lavaduct Lagoon ---


TEST_INPUT = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""


def polygon_area(vertices):
    # Shoelace algorithm
    # https://en.wikipedia.org/wiki/Shoelace_formula
    nb_vertices = len(vertices)
    sum1 = sum2 = 0

    for i in range(0, nb_vertices - 1):
        sum1 = sum1 + vertices[i][0] * vertices[i + 1][1]
        sum2 = sum2 + vertices[i][1] * vertices[i + 1][0]

    # Add xn.y1
    sum1 = sum1 + vertices[nb_vertices - 1][0] * vertices[0][1]
    # Add x1.yn
    sum2 = sum2 + vertices[0][0] * vertices[nb_vertices - 1][1]

    return abs(sum1 - sum2) / 2


def points_in_polygon(area, perimeter):
    # https://en.wikipedia.org/wiki/Pick%27s_theorem
    # A = i + (b/2) - 1 <=> i = A - (b/2) + 1
    return int(area - (perimeter/2) + 1)


def part_1(lines):
    # http://villemin.gerard.free.fr/GeomLAV/Polygone/Lacet.htm
    x = y = perimeter = 0
    vertices = [(x, y)]
    for d, size, _ in lines:
        size = int(size)
        perimeter += size
        x += size * (d == 'R') - size * (d == 'L')
        y += size * (d == 'U') - size * (d == 'D')
        vertices.append((x, y))

    return points_in_polygon(polygon_area(list(vertices)), perimeter) + perimeter


def part_2(lines):
    return part_1(map(lambda line: [{0: 'R', 1: 'D', 2: 'L', 3: 'U'}[int(line[2][-2])], int(line[2][2:7], 16), line[2]], lines))


if __name__ == '__main__':
    t1 = part_1(list(map(str.split, TEST_INPUT.splitlines())))
    assert t1 == 62, t1
    print(f"test 1: {t1}")
    lines = open('./input.txt', 'r').read().splitlines()
    r1 = part_1(list(map(str.split, lines)))
    assert r1 == 76387, r1
    print(f"#1: {r1}")
    t2 = part_2(list(map(str.split, TEST_INPUT.splitlines())))
    assert t2 == 952408144115, t2
    print(f"test 2: {t2}")
    r2 = part_2(list(map(str.split, lines)))
    assert r2 == 250022188522074, r2
    print(f"#2: {r2}")
