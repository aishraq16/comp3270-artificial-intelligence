"""Q2: implement BFS-GSA. Standard-library containers are allowed."""

from collections import deque
from support.problem import is_goal
import q1


def bfs_gsa(problem, is_goal=is_goal, successors=None):
    # Supplied defaults allow normal maze search and reuse with a new problem.
    if successors is None:
        successors = q1.successors
    # Maze states are (row, column) tuples; keep them whole in the search.
    # Use problem['start_state'], is_goal(problem, state), and successors(problem, state).
    # is_goal returns True exactly when state is any food cell; otherwise False.
    # FIFO: remove, test goal, skip explored states, mark explored, append all successors.
    # Keep duplicate frontier entries, matching the lecture BFS-GSA.
    # Return {'expanded': [...], 'path': [...]} or path=None if no goal is reachable.
    #raise NotImplementedError('Implement bfs_gsa')
    dict = {
        "expanded" : [],
        "path" : []
    }
    #1. begin w the initial state and its one-state path in the frontier
    frontier = deque([(problem["start_state"], [problem["start_state"]])])
    explored = set()
    while frontier: 
        state, path = frontier.popleft()
        #2. test for the goal when a state is removed from the frontier
        if is_goal(problem, state):
            dict["path"] = path
            return dict
        #3. if the state is already in the explored set, remove it.
        if state in explored:
            continue
        explored.add(state)
        dict["expanded"].append(state)
        for successor in successors(problem, state):
            #for each successor, append its (state, path)
            action, next_state, step_cost = successor
            frontier.append((next_state, path + [next_state]))

    #5. if frontier becomes empty without finding goal, report that no path exists
    print(f"No path exists to goal!")
    dict["path"] = None
    return dict
            
# Supplied runner: leave everything below unchanged.
# Run: python3 q2.py   |   Test: python3 q2.py --test
if __name__ == '__main__':
    import sys
    from support.grader import grade_q2

    raise SystemExit(grade_q2(bfs_gsa, sys.argv[1:]))
