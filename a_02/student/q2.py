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
    # Your Q2 code here
    raise NotImplementedError('Implement evaluate_action')

# Supplied runner: leave everything below unchanged.
if __name__ == '__main__':
    from support.runner import entry
    raise SystemExit(entry(2))
