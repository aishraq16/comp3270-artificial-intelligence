"""COMP3270 A2 Q2: complete only the marked functions."""
from q1 import successor
from q0 import manhattan

def evaluate_action(problem, state, action):
    """Return a finite int/float evaluating the result of Pacman's action.
    Use q1.successor; evaluate terminal children by their final score exactly.
    For nonterminal children consider nearest food and nearest ghost distances.
    You choose and explain weights. Handle action=None (forced pass).
    Prefer an immediate win and avoid immediate capture when a safe move exists.
    Do not modify inputs. The runner chooses the first maximum in North/East/South/West order.
    Q2 gameplay has one ghost. q0.manhattan may be reused."""
    child = successor(problem, state, 'P', action)
    if child['winner'] is not None:
        return child['score']

    pos = child['pos']
    value = child['score']
    if child['food']:
        nearest_food = min(manhattan(pos, food) for food in child['food'])
        # Each extra step to food is worse than the one-point move cost, but
        # weaker than standing next to the ghost.
        value -= 5 * nearest_food
        value -= 2 * len(child['food'])
    if child['ghosts']:
        nearest_ghost = min(manhattan(pos, ghost) for ghost in child['ghosts'].values())
        # 80 at distance 1, 40 at distance 2. Survival outweighs a shorter food path.
        if nearest_ghost == 0:
            value -= 400
        else:
            value -= 80 / nearest_ghost
    return value

# Supplied runner: leave everything below unchanged.
if __name__ == '__main__':
    from support.runner import entry
    raise SystemExit(entry(2))
