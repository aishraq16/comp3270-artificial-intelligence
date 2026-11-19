"""Q4: implement UCS-GSA. Standard-library containers are allowed."""

from heapq import heappush, heappop
from support.problem import is_goal
from support.weighted_maze import successors


def ucs_gsa(problem):
    # Use problem['start_state'], is_goal(problem, state), and successors(problem, state).
    # successors returns (action, next_state, step_cost), with positive integer costs.
    # Store (total_cost, path) entries: Python handles equal-cost path ties.
    # After removing an entry, the current state is path[-1].
    # heappush(frontier, entry) adds; heappop(frontier) removes the smallest entry.
    # Test the goal on removal, skip explored states, then append all successor paths.
    # Keep duplicate frontier entries, as in the lecture UCS-GSA.
    # Return {'expanded': [...], 'path': [...], 'cost': total_cost}.
    # If no goal is reachable, both path and cost must be None.
    #raise NotImplementedError('Implement ucs_gsa')
    dict = {
        "expanded" : [],
        "path" : [],
        "cost" : 0
    }
    #1. start with path containing initial state and total cost 0
    frontier = [(0, [problem["start_state"]])]
    explored = set()
    while frontier: 
        #2. remove state with lowest total cost. test for goal
        cost, path = heappop(frontier)
        state = path[-1]
        if is_goal(problem, state):
            dict["path"] = path
            dict["cost"] = cost
            return dict
        #3. if the state is already in the explored set, remove it.
        if state in explored:
            continue
        explored.add(state)
        dict["expanded"].append(state)
        for action, next_state, step_cost in successors(problem, state):
            #add every successor with total cost
            heappush(frontier, ((step_cost + cost, path + [next_state])))

    #5. if frontier becomes empty without finding goal, report that no path exists
    print(f"No path exists to goal!")
    dict["path"] = None
    dict["cost"] = None
    return dict

# Supplied runner: leave everything below unchanged.
# Run: python3 q4.py   |   Test: python3 q4.py --test
if __name__ == '__main__':
    import sys
    from support.grader import grade_q4

    raise SystemExit(grade_q4(ucs_gsa, sys.argv[1:]))
