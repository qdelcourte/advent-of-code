# https://adventofcode.com/2024/day/21
# --- Day 21: Keypad Conundrum ---

from collections import Counter

TEST_INPUT = """029A
980A
179A
456A
379A"""


numpad_view = [
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    ['#', '0', 'A'],
]

keypad_view = [
    ['#', '^', 'A'],
    ['<', 'v', '>']
]

numpad = {v: (x, y) for y, line in enumerate(numpad_view) for x, v in enumerate(line)}
keypad = {v: (x, y) for y, line in enumerate(keypad_view) for x, v in enumerate(line)}


def seq(pad, start, end):
    """
    Sequence between two point is generated with manhattan distance
    If it goes N * X to the right then generate an N * '>' sequence, etc.
    Optimize sequence generation by choosing y direction in some cases.
    """
    sx, sy = pad[start]
    ex, ey = pad[end]
    dx, dy = ex - sx, ey - sy
    seq_x = '>' * dx + '<' * -dx
    seq_y = 'v' * dy + '^' * -dy

    prefer_y_first = (dx > 0 and (sx, ey) != pad['#']) or (ex, sy) == pad['#']
    return (seq_y + seq_x if prefer_y_first else seq_x + seq_y) + 'A'


def part_1(lines):
    """
    Generate sequence pad by pad.
    """
    def path(pad, code):
        curr = 'A'
        sequence = ''
        for c in code:
            sequence += seq(pad, curr, c)
            curr = c
        return sequence

    return sum(
        len(path(keypad, path(keypad, path(numpad, code)))) * int(code[:-1])
        for code in lines
    )


def part_2(lines, nb_keypads):
    """
    Match and count all patterns in sequences.
    As long as the same keypad is used then some pattern will be repeated.
    In those cases just count them instead of save a big sequence in memory
    """
    def path(pad, code):
        curr = 'A'
        sequence = []
        for c in code:
            sequence.append(seq(pad, curr, c))
            curr = c
        return Counter(sequence)

    complexity = 0
    for code in lines:
        from_num_pad = path(numpad, code)

        from_dir_pad = from_num_pad
        for _ in range(nb_keypads):
            new_path = Counter()
            for pattern, cnt in from_dir_pad.items():
                new_patterns = path(keypad, pattern)
                for p in new_patterns:
                    new_patterns[p] *= cnt
                new_path.update(new_patterns)
            from_dir_pad = new_path.copy()

        complexity += sum(len(p) * cnt for p, cnt in from_dir_pad.items()) * int(code[:-1])

    return complexity


if __name__ == '__main__':
    test_input = TEST_INPUT.splitlines()
    r1 = part_1(test_input)
    assert r1 == 126384, r1
    data = open('./input.txt', 'r').read().splitlines()
    r1 = part_1(data)
    assert r1 == 105458, r1
    r2 = part_2(test_input, nb_keypads=2)
    assert r2 == 126384, r2
    r2 = part_2(data, nb_keypads=2)
    assert r2 == 105458, r2
    r2 = part_2(data, nb_keypads=25)
    assert r2 == 129551515895690, r2
