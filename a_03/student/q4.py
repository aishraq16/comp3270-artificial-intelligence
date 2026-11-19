"""COMP3270 A3 Q4: Particle filtering. Implement the functions below.
Lecture reference: C5 slides 20–23."""
from support.models import (ghost_transitions, observation_probability,
                            sample_distribution, initialise_particles)


def predict_particles(problem, particles, rng):
    """Time Passes: independently sample one successor per input particle.
    Preserve list length and input order; duplicates remain separate samples.
    Use sample_distribution once per particle. Do not mutate inputs."""
    # Your Q4 code here
    raise NotImplementedError("Implement predict_particles")


def observe_particles(problem, particles, observation, rng):
    """New Evidence: resample N particles with replacement using likelihood weights.
    Aggregate by position, INCLUDING how many particles occupy that position.
    Use sample_distribution for each of N draws. Return a new list.
    All weights zero: return initialise_particles(problem, N), without RNG.
    Inputs have N>=1. Do not mutate inputs."""
    # Your Q4 code here
    raise NotImplementedError("Implement observe_particles")


if __name__ == "__main__":
    from support.runner import main
    main(4, globals())
