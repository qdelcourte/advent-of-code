import argparse

from aocd import submit

parser = argparse.ArgumentParser()
parser.add_argument("year", type=int)
parser.add_argument("day", type=int)
parser.add_argument("answer")

if __name__ == "__main__":
    args = parser.parse_args()
    try:
        submit(args.answer, year=args.year, day=args.day)
    except Exception as err:
        print(f"Submit failed: {err}")
        raise SystemExit(1)