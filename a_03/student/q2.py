"""COMP3270 A3 Q2: Q-learning. Implement the functions below.
Lecture reference: C3 slides 15–21, including calculation practice on slide 18."""



def choose_action(q_values, state, available_actions, epsilon, rng):
    """Return an epsilon-greedy action; missing Q entries mean zero.
    For nonempty actions, call rng.random() once. If less than epsilon,
    call rng.choice(available_actions) once; otherwise choose first maximum.
    Empty actions: return None without RNG calls. Do not mutate inputs."""
    # Your Q2 code here
    raise NotImplementedError("Implement choose_action")


def q_update(q_values, state, action, reward, next_state, next_actions, alpha, gamma):
    """Return a fresh Q dictionary: preserve every existing entry and update
    only (state, action).
    Missing entries mean zero. For next_state=None, the target is reward.
    Otherwise use reward plus gamma times max Q over next_actions (zero if empty).
    Use only the arguments: no access to any transition or reward model."""
    # Your Q2 code here
    raise NotImplementedError("Implement q_update")


if __name__ == "__main__":
    from support.runner import main
    main(2, globals())
