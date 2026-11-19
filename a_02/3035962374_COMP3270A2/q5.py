"""COMP3270 A2 Q5: complete only the marked functions."""
from q1 import legal_actions, successor
from q3 import next_turn
from support.game import evaluate

def minimax(problem, state, agent='P', depth=2):
    """Return {'action': best action or None, 'value': numeric backed-up value,
            'expanded': number of expanded nodes in this full search tree}.
    Use q1.legal_actions, q1.successor, q3.next_turn and support.game.evaluate.
    Pacman maximises; every ghost minimises. depth counts full rounds.
    Terminal or depth==0: evaluate once, action=None, expanded=0.
    Otherwise expand this node (count 1), recurse on every legal action in North/East/South/West
    order or one None child for forced pass. Sum child expanded counts.
    On equal values retain the FIRST action. No pruning or memoisation in this task.
    agent is 'P' or a present ghost; depth is a nonnegative integer.
    Do not modify inputs or call random functions. Read Q5 for mid-round roots."""
    if state['winner'] is not None or depth == 0:
        return {'action': None, 'value': evaluate(problem, state), 'expanded': 0}

    actions = legal_actions(problem, state, agent) or [None]
    next_agent, next_depth = next_turn(problem, agent, depth)
    best_action = None
    best_value = None
    expanded = 1
    for action in actions:
        child = successor(problem, state, agent, action)
        result = minimax(problem, child, next_agent, next_depth)
        expanded += result['expanded']
        value = result['value']
        if best_value is None or (value > best_value if agent == 'P' else value < best_value):
            best_action = action
            best_value = value
    return {'action': best_action, 'value': best_value, 'expanded': expanded}

# Supplied runner: leave everything below unchanged.
if __name__ == '__main__':
    from support.runner import entry
    raise SystemExit(entry(5))
