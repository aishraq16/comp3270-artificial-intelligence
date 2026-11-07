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
    # Your Q5 code here
    raise NotImplementedError('Implement minimax')

# Supplied runner: leave everything below unchanged.
if __name__ == '__main__':
    from support.runner import entry
    raise SystemExit(entry(5))
