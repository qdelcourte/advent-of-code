# https://adventofcode.com/2023/day/20
# --- Day 20: Pulse Propagation ---

import math
from collections import deque

TEST_INPUT = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""

TEST_INPUT_2 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""


def parse(lines):
    modules = {}
    broadcast = []
    watch = {}
    conjonctions = []
    for line in lines:
        if 'broadcaster' in line:
            broadcast = list(map(str.strip, line.split('->')[1].split(', ')))
            continue
        [module, destinations] = line.split('->')
        module_type, module_name = module[0], module.strip()[1:]

        destinations = list(map(str.strip, destinations.split(', ')))
        for destination in destinations:
            watch.setdefault(destination, [])
            watch[destination].append(module_name)

        if module_type == '%':
            modules[module_name] = (module_type, destinations, False)
        else:
            conjonctions.append(module_name)
            modules[module_name] = (module_type, destinations)

    for conjonction in conjonctions:
        (t, d) = modules[conjonction]
        s = dict(zip(watch[conjonction], [False] * len(watch[conjonction])))
        modules[conjonction] = (t, d, s)

    return broadcast, modules


def part_1(lines):
    broadcast, modules = parse(lines)

    n_low_pulse = 0
    n_high_pulse = 0
    for i in range(1000):
        pulses = deque([(module_name, False) for module_name in broadcast])
        n_low_pulse += 1
        while pulses:
            module_name, pulse = pulses.popleft()

            if pulse:
                n_high_pulse += 1
            else:
                n_low_pulse += 1

            if module_name not in modules:
                continue

            module_type, destinations, state = modules[module_name]

            new_state = None
            if module_type == '&':
                new_state = not all(state.values())
            elif module_type == '%' and pulse is False:
                new_state = not state
                modules[module_name] = (module_type, destinations, new_state)

            for destination in destinations:
                if new_state is not None:
                    pulses.append((destination, new_state))
                    if destination in modules and modules[destination][0] == '&':
                        (t, d, s) = modules[destination]
                        s[module_name] = new_state
                        modules[destination] = (t, d, s)

    return n_low_pulse * n_high_pulse


def part_2(lines):
    broadcast, modules = parse(lines)

    # rx <- ls <- tx, dd, nz, ph
    inputs = []
    parent_module = None
    for module in modules.keys():
        if 'rx' in modules[module][1]:
            parent_module = module
            break

    for module in modules.keys():
        if parent_module in modules[module][1]:
            inputs.append(module)

    print(parent_module)
    print(inputs)
    r = {}

    i = 0
    while True:
        pulses = deque([(module_name, False) for module_name in broadcast])
        while pulses:
            module_name, pulse = pulses.popleft()
            if module_name == 'rx' and not pulse:
                rx = True

            if module_name not in modules:
                continue

            module_type, destinations, state = modules[module_name]

            new_state = None
            if module_type == '&':
                new_state = not all(state.values())
            elif module_type == '%' and pulse is False:
                new_state = not state
                modules[module_name] = (module_type, destinations, new_state)

            for destination in destinations:
                if new_state is not None:
                    if new_state and destination == 'ls':
                        if module_name not in r:
                            r[module_name] = i + 1
                        if len(r) == len(inputs):
                            print('r', r)
                            # Get minimum button presses from each inputs with high pulse
                            # {'ph': 3779, 'dd': 3889, 'nz': 3907, 'tx': 4051}
                            # and compute the minimum button presses where all inputs send high pulse
                            return math.lcm(*r.values())

                    pulses.append((destination, new_state))
                    if destination in modules and modules[destination][0] == '&':
                        (t, d, s) = modules[destination]
                        s[module_name] = new_state
                        modules[destination] = (t, d, s)

        i += 1


if __name__ == '__main__':
    t1_1 = part_1(TEST_INPUT.splitlines())
    assert t1_1 == 32000000, t1_1
    print(f"test t1_1: {t1_1}")
    t1_2 = part_1(TEST_INPUT_2.splitlines())
    assert t1_2 == 11687500, t1_2
    print(f"test t1_2: {t1_2}")
    data = open('./input.txt', 'r').read()
    r1 = part_1(data.splitlines())
    assert r1 == 869395600, r1
    print(f"#1: {r1}")
    r2 = part_2(data.splitlines())
    assert r2 == 232605773145467, r2
    print(f"#2: {r2}")
