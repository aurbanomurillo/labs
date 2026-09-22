"""Entry point that dispatches to the individual pathfinding algorithms."""

import argparse

from algorithms.brute_force.main import main as run_brute_force
from algorithms.dfs.main import main as run_dfs
from algorithms.comparison.main import main as run_comparison


def main():

    parser = argparse.ArgumentParser(
        description="Run and compare pathfinding algorithms over generated mazes."
    )
    parser.add_argument(
        "algorithm",
        choices=["brute-force", "dfs", "bfs", "both", "compare"],
        help=(
            "brute-force: exhaustive weight expansion baseline. "
            "dfs: depth-first search with backtracking. "
            "bfs: breadth-first shortest-path search. "
            "both: run bfs and dfs sequentially on the same maze. "
            "compare: benchmark bfs vs dfs over multiple mazes and plot the results."
        ),
    )

    args = parser.parse_args()

    if args.algorithm == "brute-force":
        run_brute_force()
    elif args.algorithm == "dfs":
        run_dfs()
    else:
        run_comparison([args.algorithm])


if __name__ == "__main__":
    main()
