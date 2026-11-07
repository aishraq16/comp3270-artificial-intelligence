"""COMP3270 A2 Q1: complete only the marked functions."""
from support.constants import WALL, PACMAN, FOOD, EMPTY, DIRECTIONS

def legal_actions(problem, state, agent):
    """Return legal direction labels in North, East, South, West order for agent ('P' or a ghost label).
    problem has grid, walls, start, ghosts, food, map_file. state has pos, ghosts,
    food (frozenset), score (int), winner (None, 'Pacman', 'Ghost').
    A terminal state has no legal actions. Ghosts cannot enter another ghost's cell.
    Pacman may enter a ghost's cell (it is legal but fatal). Check grid boundaries.
    Do not modify problem or state."""
    # Your Q1 code here
    #raise NotImplementedError('Implement legal_actions')
    legal_actions = []
    if state["winner"] != None: return legal_actions
    (row, col) = state["pos"] if agent == 'P' else state["ghosts"][agent]
    possible_moves = {
        "North" : (-1, 0),
        "East" : (0, 1),
        "South" : (1, 0),
        "West" : (0, -1)
    }
    for label in possible_moves.keys():
        x, y = possible_moves[label]
        future_loc = (x + row, y + col)
        if future_loc[0] < 0 or future_loc[1] < 0 or future_loc[0] >= len(problem["grid"]) or future_loc[1] >= len(problem["grid"][0]):
            continue
        if future_loc in problem["walls"] or (agent != 'P' and future_loc in state["ghosts"].values()):
            continue
        legal_actions.append(label)
    return legal_actions

def successor(problem, state, agent, action):
    # state -> pos, ghosts, food, score, winner
    """Return a NEW state after one legal action; do not modify the parent or problem.
    Copy the ghosts dictionary even if only Pacman moves. food stays a frozenset.
    None means pass, allowed only if no direction is legal. Terminal input returns
    a fresh equal state. An invalid move/pass raises ValueError.
    Pacman move/pass: -1. Check collision FIRST: -500 and winner='Ghost'.
    Otherwise Pacman eats entered food (+10); no food left gives +500 and
    winner='Pacman'. Ghost moves/pass cost 0 and never remove food.
    The PDF gives the complete rules, including collisions on food."""
    # Your Q1 code here
    #raise NotImplementedError('Implement successor')
    if action == None:
        state["score"] -= 1
        return state
    
    possible_moves = {
        "North" : (-1, 0),
        "East" : (0, 1),
        "South" : (1, 0),
        "West" : (0, -1)
    }
    
    (row, col) = state["pos"] if agent == 'P' else state["ghosts"][agent]
    x, y = possible_moves[action]
    future_loc = (x + row, y + col)




def random_action(problem, state, agent, rng):
    """Return rng.choice(legal_actions(...)), or None if there are no legal moves.
    rng is a supplied random.Random instance. Use it exactly once when moves exist,
    and zero times for pass. Do not seed, use global randomness, or modify inputs."""
    # Your Q1 code here
    raise NotImplementedError('Implement random_action')

# Supplied runner: leave everything below unchanged.
if __name__ == '__main__':
    from support.runner import entry
    raise SystemExit(entry(1))
