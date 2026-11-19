"""COMP3270 A2 Q4: complete only the marked functions."""
from q1 import successor, legal_actions
from q0 import manhattan

def _evaluate(problem, state, action, include_exits):
    """Shared Q4 evaluation. The extra feature is Pacman's legal exit count."""
    child = successor(problem, state, 'P', action)
    if child['winner'] is not None:
        return child['score']

    pos = child['pos']
    value = child['score']
    if child['food']:
        nearest_food = min(manhattan(pos, food) for food in child['food'])
        value -= 5 * nearest_food
        value -= 2 * len(child['food'])
    for ghost in child['ghosts'].values():
        distance = manhattan(pos, ghost)
        if distance == 0:
            value -= 400
        else:
            value -= 60 / distance
    if include_exits:
        # More legal directions after this move means a better chance to dodge.
        value += 15 * len(legal_actions(problem, child, 'P'))
    return value

def evaluate_action(problem, state, action):
    """Same return contract as Q2, now with one to four ghosts.
    Evaluate terminal child by its final score exactly. For nonterminal children
    consider food and all ghosts, and explain one additional risk/escape feature.
    Reuse your Q2 reasoning/helpers where useful; do not duplicate the game engine.
    Prefer an immediate win and avoid immediate capture when a safe move exists.
    Do not modify inputs. action=None is forced pass."""
    return _evaluate(problem, state, action, True)

def evaluate_action_without_feature(problem, state, action):
    """Return your Q4 evaluation with ONLY the additional risk/escape feature removed.
    Keep the same other features, weights and exact terminal-score handling.
    Used for --inspect --ablate and the written comparison. Do not modify inputs.
    You may share a small helper with evaluate_action rather than duplicate code."""
    return _evaluate(problem, state, action, False)

# Supplied runner: leave everything below unchanged.
if __name__ == '__main__':
    from support.runner import entry
    raise SystemExit(entry(4))
