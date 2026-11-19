"""Q3: implement DFS-GSA. Standard-library containers are allowed."""

from collections import deque
from support.problem import is_goal
import q1


def dfs_gsa(problem, is_goal=is_goal, successors=None):
    # Supplied defaults allow normal maze search and reuse with a new problem.
    if successors is None:
        successors = q1.successors
    # Maze states are (row, column) tuples; keep them whole in the search.
    # Use problem['start_state'], is_goal(problem, state), and successors(problem, state).
    # LIFO: remove, test goal, skip explored states, mark explored, append all successors.
    # Keep duplicate frontier entries and the supplied successor order, as in the lecture.
    # Return {'expanded': [...], 'path': [...]} or path=None if no goal is reachable.
    #raise NotImplementedError('Implement dfs_gsa')

    dict = {
            "expanded" : [],
            "path" : []
        }
    frontier = deque([(problem["start_state"], [problem["start_state"]])])        
    explored = set()
    while frontier: 
        state, path = frontier.pop()            
        if is_goal(problem, state):
            dict["path"] = path
            return dict
        if state in explored:
            continue
        explored.add(state)
        dict["expanded"].append(state)
        for action, next_state, step_cost in successors(problem, state):
            frontier.append((next_state, path + [next_state]))
    
    print(f"No path exists to goal!")
    dict["path"] = None
    return dict


# Supplied runner: leave everything below unchanged.
# Run: python3 q3.py   |   Test: python3 q3.py --test
if __name__ == '__main__':
    import sys
    from support.grader import grade_q3

    raise SystemExit(grade_q3(dfs_gsa, sys.argv[1:]))
