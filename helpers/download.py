import argparse

import copier
from aocd import get_puzzle

parser = argparse.ArgumentParser()
parser.add_argument("year", type=int)
parser.add_argument("day", type=str)

if __name__ == "__main__":
    args = parser.parse_args()
    try:
        puzzle = get_puzzle(year=args.year, day=int(args.day))
        copier.run_copy(
            src_path="./template",
            data={
                'year': args.year,
                'day': args.day,
                'puzzle_name': puzzle.title,
                'puzzle_input_data': puzzle.input_data,
                'puzzle_example_data_1': puzzle.examples[0].input_data,
                'puzzle_example_answer_1': puzzle.examples[0].answer_a,
            }
        )
    except Exception as err:
        # Catch exceptions so that Copier doesn't clean up directories
        print(f"Download of input failed: {err}")
        raise SystemExit(1)