# AoC

This repository contains my personal solutions to the [Advent Of Code](https://adventofcode.com) challenges.

Use:
- [UV](https://github.com/astral-sh/uv): Python package manager
- [Advent of code data](https://github.com/wimglenn/advent-of-code-data): Python tool to fetch data from AoC website
- [Copier](https://github.com/copier-org/copier): Tool to generate project template

## Command lines

Create template fast ! (By default on the current date) 
You have to add your [session ID](https://github.com/wimglenn/advent-of-code-data#quickstart) in env

    make create
    make create YEAR=2025 DAY=1

Run a script ! (By default on the current date)

    make run
    make run YEAR=2025 DAY=1
