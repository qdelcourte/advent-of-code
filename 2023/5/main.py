# https://adventofcode.com/2023/day/5
# --- Day 5: If You Give A Seed A Fertilizer ---

def parse():
    seeds, maps, current_key = [], {}, None
    for line in lines:
        if 'seeds:' in line:
            seeds = list(map(int, line.replace('seeds: ', '').split(' ')))
            continue
        elif line == '' or 'map:' in line:
            current_key = line
            continue

        if current_key:
            maps.setdefault(current_key, [])
            # [destination range start, source range start, range length]
            maps[current_key].append(list(map(int, line.split(' '))))

    return seeds, maps


def part_1():
    seeds, maps = parse()

    def get_destination(seed, ranges):
        for r in ranges:
            if r[1] > seed:
                continue
            if r[1] <= seed <= r[1] + r[2] - 1:
                return (seed - r[1]) + r[0]
            return seed
        return seed

    for m in maps.keys():
        ranges = sorted(maps[m], key=lambda x: x[1], reverse=True)
        seeds = [get_destination(seed, ranges) for seed in seeds]

    return min(seeds)


def part_2():
    seeds, maps = parse()
    seeds = [seeds[i:i + 2] for i in range(0, len(seeds), 2)]

    def get_source(source, ranges):
        for r in ranges:
            if r[0] > source:
                continue
            if r[0] <= source <= r[0] + r[2] - 1:
                return (source - r[0]) + r[1]
            return source
        return source

    def in_seeds(seed_to_check):
        for seed, incr in seeds:
            if seed <= seed_to_check <= seed+incr:
                return True
        return False

    key_reversed = list(reversed(maps.keys()))
    for m in key_reversed:
        maps[m] = list(sorted(maps[m], key=lambda x: x[0], reverse=True))

    location = 0
    while location < 4018529087:
        seed = location
        for m in key_reversed:
            seed = get_source(seed, maps[m])

        if in_seeds(seed):
            print('success !!!', location, seed)
            return location
        location += 1


if __name__ == '__main__':
    lines = open('./input.txt', 'r').read().splitlines()
    r1 = part_1()
    assert r1 == 175622908, r1
    print(f"#1: {r1}")
    r2 = part_2()
    assert r2 == 5200543, r2
    print(f"#2: {r2}")
