# AoC
![](https://img.shields.io/badge/stars%20⭐-144-yellow)

This repository contains my personal solutions to the [Advent Of Code](https://adventofcode.com) challenges.

Use:
- [UV](https://github.com/astral-sh/uv): Python package manager
- [Advent of code data](https://github.com/wimglenn/advent-of-code-data): Python tool to fetch data from AoC website
- [Copier](https://github.com/copier-org/copier): Tool to generate project template

## Command lines

Retrieve your session from your browser after logging in to Advent of Code:

    make session

When a single valid token is found, it is saved to `~/.config/aocd/token` if
that file does not already exist. `aocd` reads this file automatically for
`make create` and `make submit`. No session script or environment variable is
required; the token stays outside the repository.

Create template fast ! (By default on the current date)

    make create
    make create YEAR=2025 DAY=01

Run a script ! (By default on the current date)

    make run
    make run YEAR=2025 DAY=01

If an error appear try to use LEGACY param to run an old solution (not yet migrated)

    make run YEAR=2025 DAY=1 LEGACY=1

Submit your answer like this:    
    
    make submit ANSWER=xxxx
    make submit YEAR=2025 DAY=01 ANSWER=xxxx
