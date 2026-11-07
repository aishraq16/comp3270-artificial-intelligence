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
    # Your Q6 code here
    raise NotImplementedError('Implement expectimax')

# Supplied runner: leave everything below unchanged.
if __name__ == '__main__':
    from support.runner import entry
    raise SystemExit(entry(6))
