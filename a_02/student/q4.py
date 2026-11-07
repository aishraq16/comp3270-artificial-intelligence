"""COMP3270 A2 Q4: complete only the marked functions."""
from q1 import successor, legal_actions
from q0 import manhattan

def evaluate_action(problem, state, action):
    """Same return contract as Q2, now with one to four ghosts.
    Evaluate terminal child by its final score exactly. For nonterminal children
    consider food and all ghosts, and explain one additional risk/escape feature.
    Reuse your Q2 reasoning/helpers where useful; do not duplicate the game engine.
    Prefer an immediate win and avoid immediate capture when a safe move exists.
    Do not modify inputs. action=None is forced pass."""
    # Your Q4 code here
    raise NotImplementedError('Implement evaluate_action')

def evaluate_action_without_feature(problem, state, action):
    """Return your Q4 evaluation with ONLY the additional risk/escape feature removed.
    Keep the same other features, weights and exact terminal-score handling.
    Used for --inspect --ablate and the written comparison. Do not modify inputs.
    You may share a small helper with evaluate_action rather than duplicate code."""
    # Your Q4 comparison code here
    raise NotImplementedError('Implement evaluate_action_without_feature')

# Supplied runner: leave everything below unchanged.
if __name__ == '__main__':
    from support.runner import entry
    raise SystemExit(entry(4))
