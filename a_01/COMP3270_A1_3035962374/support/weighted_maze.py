"""Supplied cell-entry costs for Q4. No edits needed."""
import q1
from support.problem import load_maze


def load_weighted_case(path):
    return load_maze(path, weighted=True)


def successors(problem, state):
    return [(action, child, problem['cell_costs'].get(child, 1))
            for action, child, _ in q1.successors(problem, state)]
