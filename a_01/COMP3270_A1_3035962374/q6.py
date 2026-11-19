"""Q6: guide the collect-all-food search with A*-GSA."""

from heapq import heappush, heappop
from q5 import initial_state, pacman_position, remaining_food, is_goal, successors
from support.search_order import path_key as make_path_key


def path_key(path):
    # Supplied: comparable key for lecture-style whole-path tie breaking.
    return make_path_key(path, pacman_position, remaining_food)


def heuristic(problem, state):
    # Use the Q5 display functions to inspect your state.
    # Return the largest Manhattan distance to any remaining food, or 0 if none.
    # Return an integer and do not modify problem or state.
    #raise NotImplementedError('Implement heuristic')
    r, c = pacman_position(state)
    foods = remaining_food(state)
    manhattan_distances = [abs(r - fr) + abs(c - fc) for fr, fc in foods]
    return max(manhattan_distances, default = 0)

def a_star_gsa(problem):
    # Use entries (f, path_key(path), path), where f = g + heuristic(problem, state).
    # Start with the one-state path and its heuristic as the initial priority.
    # On removal: test goal, skip explored states, then mark and record expansion.
    # Add every successor, keeping duplicates and the supplied move order.
    # Lecture update: new_f = f + step_cost - heuristic(problem, state)
    #                                      + heuristic(problem, child).
    # Return {'expanded': [...], 'path': [...]} using complete Q5 states.
    # If no solution exists, return path=None.
    #raise NotImplementedError('Implement a_star_gsa')
    result = {
        "expanded" : [], 
        "path" : None
    }
    start = initial_state(problem)
    path = [start]
    frontier = [ (heuristic(problem, start), path_key(path), path) ]
    explored = set()
    while frontier:
        f, _, path = heappop(frontier)
        state = path[-1]
        if is_goal(problem, state):
            result["path"] = path
            return result
        if state in explored:
            continue
        explored.add(state)
        result["expanded"].append(state)
        #action, child_state, step_cost)
        for _, child_state, step_cost in successors(problem, state):
            new_f = f + step_cost - heuristic(problem, state) + heuristic(problem, child_state)
            child_path = path + [child_state]
            heappush(frontier, (new_f, path_key(child_path), child_path))
    return result
            



# Supplied runner: leave everything below unchanged.
# Run: python3 q6.py   |   Test: python3 q6.py --test
if __name__ == '__main__':
    import sys
    from support.collect_food import run

    raise SystemExit(run(sys.modules[__name__], sys.argv[1:], question='Q6'))
