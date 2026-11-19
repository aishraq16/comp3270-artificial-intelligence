"""Q5: choose a state representation and collect all food using BFS-GSA."""

from q2 import bfs_gsa as search_bfs
from q1 import successors as position_successors


def initial_state(problem):
    # Inputs: problem['grid'], problem['food_positions'] (tuple of coordinate tuples),
    # and problem['pacman_start'] (coordinate tuple). Do not modify problem.
    # Return your immutable, hashable state containing position and remaining food.
    #raise NotImplementedError('Implement initial_state')
    return (problem["pacman_start"], frozenset(problem["food_positions"]))

def pacman_position(state):
    # Return the (row, column) tuple from your chosen state representation.
    #raise NotImplementedError('Implement pacman_position')
    pos, _ = state
    return pos 

def remaining_food(state):
    # Return a tuple of remaining food coordinate tuples, in row/column order.
    # This display format does not constrain how you store food inside state.
    #raise NotImplementedError('Implement remaining_food')
    _, food_pos = state
    return tuple(sorted(food_pos))


def is_goal(problem, state):
    # Return True exactly when all food has been eaten; otherwise False.
    #raise NotImplementedError('Implement is_goal')
    if not remaining_food(state):
        return True
    return False

def successors(problem, state):
    # Return [(action, child_state, 1), ...] in North, East, South, West order.
    # position_successors(problem, pacman_position(state)) supplies legal moves.
    # Entering a food cell removes that food. Do not modify state or problem.
    #raise NotImplementedError('Implement successors')
    successors = []
    parent_pos = pacman_position(state)
    parent_food = remaining_food(state)
    for action, next_pos, step_cost in position_successors(problem, parent_pos):
        child_food = frozenset(parent_food) - {next_pos}
        child_state = (next_pos, child_food)
        successors.append(
            (action, child_state, step_cost)
        )
    return successors


def bfs_gsa(problem):
    # Supplied adapter: reuse Q2 with Q5's problem definition.
    return search_bfs(problem, is_goal=is_goal, successors=successors)


# Supplied runner: leave everything below unchanged.
# Run: python3 q5.py   |   Test: python3 q5.py --test
if __name__ == '__main__':
    import sys
    from support.collect_food import run

    raise SystemExit(run(sys.modules[__name__], sys.argv[1:]))
