"""COMP3270 A3 Q3: Exact filtering. Implement the functions below.
Lecture reference: C5 slides 9–12; examples and practice on slides 13–16."""
from support.models import ghost_transitions, observation_probability


def predict(problem, belief):
    """Time Passes: return predicted belief over every state.
    belief is a normalised dict over all states. Do not mutate inputs."""
    # Your Q3 code here
    raise NotImplementedError("Implement predict")


def observe(problem, belief, observation):
    """New Evidence: weight the given belief by the observation likelihood.
    Return a normalised dict over all states. Do not move the ghost here.
    If normalising constant is zero, raise ValueError. No input mutation."""
    # Your Q3 code here
    raise NotImplementedError("Implement observe")


if __name__ == "__main__":
    from support.runner import main
    main(3, globals())
