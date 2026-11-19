"""COMP3270 A2 Q1: complete only the marked functions."""
from support.constants import WALL, PACMAN, FOOD, EMPTY, DIRECTIONS

def legal_actions(problem, state, agent):
    """Return legal direction labels in North, East, South, West order for agent ('P' or a ghost label).
    problem has grid, walls, start, ghosts, food, map_file. state has pos, ghosts,
    food (frozenset), score (int), winner (None, 'Pacman', 'Ghost').
    A terminal state has no legal actions. Ghosts cannot enter another ghost's cell.
    Pacman may enter a ghost's cell (it is legal but fatal). Check grid boundaries.
    Do not modify problem or state."""
    if state['winner'] is not None:
        return []
    row, col = state['pos'] if agent == 'P' else state['ghosts'][agent]
    height = len(problem['grid'])
    width = len(problem['grid'][0])
    blocked = {pos for label, pos in state['ghosts'].items() if label != agent}
    actions = []
    for label, (drow, dcol) in DIRECTIONS:
        nxt = (row + drow, col + dcol)
        if nxt[0] < 0 or nxt[1] < 0 or nxt[0] >= height or nxt[1] >= width:
            continue
        if nxt in problem['walls']:
            continue
        if agent != 'P' and nxt in blocked:
            continue
        actions.append(label)
    return actions

def successor(problem, state, agent, action):
    """Return a NEW state after one legal action; do not modify the parent or problem.
    Copy the ghosts dictionary even if only Pacman moves. food stays a frozenset.
    None means pass, allowed only if no direction is legal. Terminal input returns
    a fresh equal state. An invalid move/pass raises ValueError.
    Pacman move/pass: -1. Check collision FIRST: -500 and winner='Ghost'.
    Otherwise Pacman eats entered food (+10); no food left gives +500 and
    winner='Pacman'. Ghost moves/pass cost 0 and never remove food.
    The PDF gives the complete rules, including collisions on food."""
    child = {
        'pos': state['pos'],
        'ghosts': dict(state['ghosts']),
        'food': state['food'],
        'score': state['score'],
        'winner': state['winner'],
    }
    if state['winner'] is not None:
        return child

    legal = legal_actions(problem, state, agent)
    if action is None:
        if legal:
            raise ValueError('A pass is allowed only when no direction is legal.')
    elif action not in legal:
        raise ValueError('Action is not a legal move.')
    else:
        row, col = state['pos'] if agent == 'P' else state['ghosts'][agent]
        delta = dict(DIRECTIONS)[action]
        nxt = (row + delta[0], col + delta[1])
        if agent == 'P':
            child['pos'] = nxt
        else:
            child['ghosts'][agent] = nxt

    if agent == 'P':
        child['score'] -= 1
    if child['pos'] in child['ghosts'].values():
        child['score'] -= 500
        child['winner'] = 'Ghost'
    elif agent == 'P' and action is not None and child['pos'] in child['food']:
        child['food'] = child['food'] - {child['pos']}
        child['score'] += 10
        if not child['food']:
            child['score'] += 500
            child['winner'] = 'Pacman'
    return child

def random_action(problem, state, agent, rng):
    """Return rng.choice(legal_actions(...)), or None if there are no legal moves.
    rng is a supplied random.Random instance. Use it exactly once when moves exist,
    and zero times for pass. Do not seed, use global randomness, or modify inputs."""
    actions = legal_actions(problem, state, agent)
    if not actions:
        return None
    return rng.choice(actions)

# Supplied runner: leave everything below unchanged.
if __name__ == '__main__':
    from support.runner import entry
    raise SystemExit(entry(1))
