"""COMP3270 A2 Q6: complete only the marked functions."""
from q1 import legal_actions, successor
from q3 import next_turn
from support.game import evaluate

def expectimax(problem, state, agent='P', depth=2):
    """Same input/result contract and expanded-node counting as Q5.
    Pacman maximises, retaining the first equally best action. At each ghost node,
    return the arithmetic mean of ALL legal children (uniform conditional choice).
    Ghost-node result action is None because it describes a distribution.
    A forced pass has one child, probability 1. Terminal/depth==0 uses the supplied
    evaluate function. Do not sample random actions inside search.
    Reuse Q1/Q3 helpers. Do not mutate inputs; no pruning or memoisation."""
    if state['winner'] is not None or depth == 0:
        return {'action': None, 'value': evaluate(problem, state), 'expanded': 0}

    actions = legal_actions(problem, state, agent) or [None]
    next_agent, next_depth = next_turn(problem, agent, depth)
    best_action = None
    best_value = None
    total = 0
    expanded = 1
    for action in actions:
        child = successor(problem, state, agent, action)
        result = expectimax(problem, child, next_agent, next_depth)
        expanded += result['expanded']
        total += result['value']
        if agent == 'P' and (best_value is None or result['value'] > best_value):
            best_action = action
            best_value = result['value']
    if agent == 'P':
        return {'action': best_action, 'value': best_value, 'expanded': expanded}
    return {'action': None, 'value': total / len(actions), 'expanded': expanded}

# Supplied runner: leave everything below unchanged.
if __name__ == '__main__':
    from support.runner import entry
    raise SystemExit(entry(6))
