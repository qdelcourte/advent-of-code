# https://adventofcode.com/2023/day/15
# --- Day 15: Lens Library ---

from functools import reduce

TEST_INPUT = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


def hash(steps):
    return sum([
        reduce(lambda acc, char: ((acc + ord(char)) * 17) % 256, list(step), 0)
        for step in steps
    ])


def test_1():
    return hash(TEST_INPUT.replace('\n', '').split(','))


def part_1():
    return hash(data.replace('\n', '').split(','))


def solve2(steps):
    boxes: dict = {}
    for step in steps:
        if '-' in step:
            label = step[:-1]
            box_number = hash([label])
            boxes.setdefault(box_number, [])
            boxes[box_number] = list(filter(lambda lens: lens[0] != label, boxes[box_number]))
        else:
            label, focal_length = step.split('=')
            box_number = hash([label])
            boxes.setdefault(box_number, [])
            for i, (lens_label, _) in enumerate(boxes[box_number]):
                if lens_label == label:
                    boxes[box_number][i] = (label, focal_length)
                    break
            else:
                boxes[box_number].append((label, focal_length))

    return sum(
        (1 + int(box_number)) * slot * int(focal_length)
        for box_number, box in boxes.items()
        for slot, (label, focal_length) in enumerate(box, start=1))


def test_2():
    return solve2(TEST_INPUT.replace('\n', '').split(','))


def part_2():
    return solve2(data.replace('\n', '').split(','))


if __name__ == '__main__':
    t1 = test_1()
    assert t1 == 1320, t1
    print(f"test 1: {t1}")
    data = open('./input.txt', 'r').read()
    r1 = part_1()
    assert r1 == 506869, r1
    print(f"#1: {r1}")
    t2 = test_2()
    assert t2 == 145, t2
    print(f"test 2: {t2}")
    r2 = part_2()
    assert r2 == 271384, r2
    print(f"#2: {r2}")
