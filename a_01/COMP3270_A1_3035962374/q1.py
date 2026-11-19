"""Q1: check maze positions and generate legal successors."""

from support.constants import WALL, PACMAN, FOOD, EMPTY


def is_valid_position(problem, state):
    # Q1(a): return True if state is inside the grid and is not a WALL, else False.
    # state is a (row, column) tuple of integers; it may be outside the grid.
    # problem['grid'] is a nonempty list of equal-length row strings.
    # Rows and columns start at zero. Do not modify either argument.
    #raise NotImplementedError('Implement is_valid_position')
    row, col = state
    if row < 0 or row >= len(problem["grid"]):
        return False
    if col < 0 or col >= len(problem["grid"][0]):
        return False
    if problem["grid"][row][col] == WALL:
        return False
    return True
    

def successors(problem, state):
    # Q1(b): state is a valid (row, column) tuple.
    # Use is_valid_position to check each neighbouring position.
    # Return a list of (action, next_state, 1) tuples in North, East, South, West order.
    # next_state is also a (row, column) tuple. Do not modify either argument.
    #raise NotImplementedError('Implement successors')
    successors = []
    row, col = state
    if is_valid_position(problem, (row - 1, col)): successors.append(("North", (row - 1, col), 1))
    if is_valid_position(problem, (row, col + 1)): successors.append(("East", (row, col + 1), 1))
    if is_valid_position(problem, (row + 1, col)): successors.append(("South", (row + 1, col), 1))
    if is_valid_position(problem, (row, col - 1)): successors.append(("West", (row, col - 1), 1))
    return successors

# Supplied runner: leave everything below unchanged.
# Run: python3 q1.py   |   Test: python3 q1.py --test
if __name__ == '__main__':
    import sys
    from support.grader import grade_q1

    raise SystemExit(grade_q1(is_valid_position, successors, sys.argv[1:]))
