# Pathfinding Algorithms Lab

[![Python](https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A comparative study of pathfinding algorithms implemented from scratch in Python, benchmarked against procedurally generated mazes under uniform conditions.

Each algorithm is built with a consistent object-oriented design around a shared maze abstraction, which makes it possible to compare search strategies fairly — same maze, same rules, different search logic.

---

## Overview

| Algorithm | Location | Strategy |
|---|---|---|
| **Brute Force** | [`algorithms/brute_force`](algorithms/brute_force) | Exhaustive weight expansion over every reachable cell, with no heuristics. Serves as the baseline. |
| **DFS** | [`algorithms/dfs`](algorithms/dfs) | Depth-first traversal that walks the maze and backtracks at dead ends. |
| **BFS / Compare** | [`algorithms/comparison`](algorithms/comparison) | Breadth-first shortest-path search, plus a benchmarking mode that runs BFS and DFS side by side and plots their execution times. |

All mazes are generated procedurally via a randomized DFS carving algorithm, ensuring reproducible and consistently complex layouts across every run.

## Repository structure

```text
labs/
├── main.py                     # Root CLI — dispatches to each algorithm
├── algorithms/
│   ├── brute_force/
│   │   └── main.py             # Exhaustive baseline search
│   ├── dfs/
│   │   └── main.py             # Depth-first search with backtracking
│   └── comparison/
│       └── main.py             # BFS, DFS and benchmarking mode
├── requirements.txt
├── pyproject.toml
├── LICENSE
└── README.md
```

## Getting started

### Requirements

- Python 3.10+

### Installation

```bash
git clone https://github.com/aurbanomurillo/labs.git
cd labs
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Usage

Run any algorithm through the root entry point:

```bash
python main.py brute-force   # Exhaustive baseline search
python main.py dfs           # Depth-first search with backtracking
python main.py bfs           # Breadth-first shortest-path search
python main.py both          # Run BFS and DFS sequentially on the same maze
python main.py compare       # Benchmark BFS vs DFS over 50 mazes and plot results
```

Each algorithm module can also be run standalone, e.g. `python -m algorithms.dfs.main`.

### Reading the output

| Symbol | Meaning |
|---|---|
| 🟦 | Start |
| 🟩 | Goal |
| ⬛ | Wall |
| ⬜ | Empty cell |
| 🟧 | Explored cell |
| 🟥 | Shortest path found |

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

## Author

**Antonio Urbano Murillo**
Email: [urbano@alu.comillas.edu](mailto:urbano@alu.comillas.edu)
LinkedIn: [in/a-urbano](https://www.linkedin.com/in/a-urbano)
