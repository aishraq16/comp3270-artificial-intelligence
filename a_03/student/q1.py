"""COMP3270 A3 Q1: Value iteration. Implement the functions below.
Lecture reference: C2 slides 33–34."""
from support.models import actions, transitions


def action_value(problem, state, action, values):
    """Return Q(s,a) from the supplied value dictionary. Use discount from problem.
    None is terminal and has value zero. Do not change any input."""
    # Your Q1 code here
    #raise NotImplementedError("Implement action_value")
    if state is None:
        return 0
    q_val = 0
    for p, next_state, reward in transitions(problem, state, action):
        next_val = 0.0 if next_state is None else values[next_state]
        q_val += p * (reward + problem["discount"]*next_val)
    return q_val
    

def value_iteration(problem, iterations):
    """Return all non-wall state values after exactly iterations synchronous sweeps.
    Start with V0=0, including exit cells. iterations is a nonnegative integer.
    Use action_value. Do not change problem."""
    # Your Q1 code here
    #raise NotImplementedError("Implement value_iteration")
    #build the initial dictionary 
    values = {state : 0.0 for state in problem["states"] if state is not None}
    for i in range(iterations):
        new_values = {}
        for state in problem["states"]:
            if state is None:
                continue
            q_values = []
            for action in actions(problem, state):
                q_val = action_value(problem, state, action, values)
                q_values.append(q_val)
            if len(q_values) != 0: 
                new_values[state] = max(q_values)
            else: new_values[state] = 0 
        values = new_values
    return values

if __name__ == "__main__":
    from support.runner import main
    main(1, globals())
