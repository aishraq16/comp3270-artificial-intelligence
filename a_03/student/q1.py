"""COMP3270 A3 Q1: Value iteration. Implement the functions below.
Lecture reference: C2 slides 33–34."""
from support.models import actions, transitions


def action_value(problem, state, action, values):
    """Return Q(s,a) from the supplied value dictionary. Use discount from problem.
    None is terminal and has value zero. Do not change any input."""
    # Your Q1 code here
    raise NotImplementedError("Implement action_value")


def value_iteration(problem, iterations):
    """Return all non-wall state values after exactly iterations synchronous sweeps.
    Start with V0=0, including exit cells. iterations is a nonnegative integer.
    Use action_value. Do not change problem."""
    # Your Q1 code here
    raise NotImplementedError("Implement value_iteration")


if __name__ == "__main__":
    from support.runner import main
    main(1, globals())
