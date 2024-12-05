# https://adventofcode.com/2024/day/4
# --- Day 4: Ceres Search ---

import numpy as np
import re

TEST_INPUT = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""


def part_1(lines):
    regex = re.compile('(?=(XMAS|SAMX))')
    d = np.array([list(line) for line in lines], str)

    def search_xmas(dataset):
        res = sum(len(regex.findall(''.join(line))) for line in dataset)

        # Search in diagonal
        for i in range(-dataset.shape[1] + 1, dataset.shape[1]):
            res += len(regex.findall(''.join(dataset.diagonal(offset=i))))

        return res

    return sum(search_xmas(dataset) for dataset in [d, np.rot90(d)])


def part_2(lines):
    regex = re.compile('(?=(MAS|SAM))')
    d = np.array([list(line) for line in lines], str)

    def search_x_mas(dataset):
        search_matrix = np.zeros(dataset.shape)

        for k in range(-dataset.shape[1] + 1, dataset.shape[1]):
            for m in regex.finditer(''.join(dataset.diagonal(offset=k))):
                if k < 0:
                    x = m.start(1) + 1
                    y = m.end(1) - (1 + k) - 1
                elif k == 0:
                    x = m.start(1) + 1
                    y = m.end(1) - 2
                else:
                    x = m.start(1) + (1 + k)
                    y = m.end(1) - 2
                search_matrix[y][x] = 1

        return search_matrix.astype(int)

    return np.count_nonzero(np.bitwise_and(*[search_x_mas(d), np.fliplr(search_x_mas(np.fliplr(d)))]))


if __name__ == '__main__':
    test_input = TEST_INPUT.splitlines()
    r1 = part_1(test_input)
    assert r1 == 18, r1
    data = open('./input.txt', 'r').read().splitlines()
    r1 = part_1(data)
    assert r1 == 2378, r1
    r2 = part_2(test_input)
    assert r2 == 9, r2
    r2 = part_2(data)
    assert r2 == 1796, r2
