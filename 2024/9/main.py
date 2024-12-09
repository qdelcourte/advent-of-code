# https://adventofcode.com/2024/day/9
# --- Day 9: Disk Fragmenter ---

TEST_INPUT = "2333133121414131402"
FREE_SPACE = '.'


def checksum(filesystem):
    return sum(i * block for i, block in enumerate(filesystem) if block != FREE_SPACE)


def to_blocks(filesystem):
    id = 0
    blocks = []
    for i, j in enumerate(filesystem):
        if i % 2 == 0:
            blocks.extend([id]*int(j))
            id += 1
        else:
            blocks.extend([FREE_SPACE]*int(j))
    return blocks


def part_1(entry):
    filesystem = []
    blocks = to_blocks(entry)
    b = list(filter(lambda x: x != FREE_SPACE, blocks))
    l = len(b)
    i = 1
    for k in blocks:
        if k == FREE_SPACE:
            filesystem.append(b[-i])
            i += 1
        else:
            filesystem.append(k)
        if l == len(filesystem):
            break

    return checksum(filesystem)


def part_2(entry):
    filesystem = to_blocks(entry)

    files = {}
    for b in filesystem:
        if b == '.':
            continue
        files.setdefault(b, 0)
        files[b] += 1

    for f in reversed(files.keys()):
        file_idx = filesystem.index(f)
        first_space_index = filesystem.index(FREE_SPACE)
        if file_idx < first_space_index:
            continue

        free_space_count = 0
        for i, b in enumerate(filesystem[first_space_index:], start=first_space_index):
            if b == FREE_SPACE:
                free_space_count += 1
            else:
                if free_space_count:
                    file_len = files[f]
                    if file_len <= free_space_count:
                        if file_idx < i - free_space_count:
                            continue
                        filesystem[file_idx:file_idx + file_len] = [FREE_SPACE] * file_len
                        filesystem[i - free_space_count:i - free_space_count + file_len] = [f] * file_len
                        break
                free_space_count = 0

    return checksum(filesystem)


if __name__ == '__main__':
    test_input = TEST_INPUT
    r1 = part_1(test_input)
    assert r1 == 1928, r1
    data = open('./input.txt', 'r').read()
    r1 = part_1(data)
    assert r1 == 6216544403458, r1
    r2 = part_2(test_input)
    assert r2 == 2858, r2
    r2 = part_2(data)
    assert r2 == 6237075041489, r2
