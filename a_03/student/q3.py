"""COMP3270 A3 Q3: Exact filtering. Implement the functions below.
Lecture reference: C5 slides 9–12; examples and practice on slides 13–16."""
from support.models import ghost_transitions, observation_probability


def predict(problem, belief):
    """Time Passes: return predicted belief over every state.
    belief is a normalised dict over all states. Do not mutate inputs."""
    # Your Q3 code here
    #raise NotImplementedError("Implement predict")
    new_belief = {state : 0.0 for state in problem["states"]}
    for state in problem["states"]:
        for next_state, p in ghost_transitions(problem, state):
            new_belief[state] += p * belief[next_state]
    return new_belief


def observe(problem, belief, observation):
    """New Evidence: weight the given belief by the observation likelihood.
    Return a normalised dict over all states. Do not move the ghost here.
    If normalising constant is zero, raise ValueError. No input mutation."""
    # Your Q3 code here
    #raise NotImplementedError("Implement observe")
    z = sum([belief[state] * observation_probability(problem, state, observation)for state in problem["states"]])
    new_belief = {state : 0.0 for state in problem["states"]}
    for state in problem["states"]:
        new_belief[state] = observation_probability(problem, state, observation) * belief[state] / z
    return new_belief



if __name__ == "__main__":
    from support.runner import main
    main(3, globals())
