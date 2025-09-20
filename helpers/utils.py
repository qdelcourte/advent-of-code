import os

def read_input_from_main(execution_file: str):
    return open(os.path.join(os.path.dirname(execution_file), "input.txt"), 'r').read().splitlines()

def pprint_matrix(m):
    """
    Pretty print matrix
    """
    for r in range(len(m)):  # rows
        for c in range(len(m[r])):  # columns
            print(m[r][c], " ", sep="", end="")
        print()
    print("-------------")

def str_to_matrix(data: str):
    return [list(map(int, line)) for line in data]
