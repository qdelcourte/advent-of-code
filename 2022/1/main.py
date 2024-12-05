# https://adventofcode.com/2022/day/1
# --- Day 1: Calorie Counting ---

def part_1():
    return max([sum(map(int, line.strip().split('\n'))) for line in lines])


def part_2():
    return sum(sorted([sum(map(int, line.strip().split('\n'))) for line in lines], reverse=True)[:3])


if __name__ == '__main__':
    lines = open('./input.txt', 'r').read().split('\n\n')
    r1 = part_1()
    assert r1 == 66306, r1
    print(f"#1: {r1}")
    r2 = part_2()
    assert r2 == 195292, r2
    print(f"#2: {r2}")
