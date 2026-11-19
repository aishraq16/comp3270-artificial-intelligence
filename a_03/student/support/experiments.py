"""Supplied training and observation loops; edit only q1.py through q4.py."""
import random
from .models import (actions, sample_transition, uniform_belief,
                     initialise_particles, particle_belief)


def train(problem, choose_action, q_update, episodes=1000, seed=0):
    # Separate streams: environmental noise is not affected by action RNG calls.
    policy_rng, world_rng = random.Random(seed), random.Random(seed + 10000)
    q_values = {}
    visits = {}
    completed = 0
    for episode in range(episodes):
        state = problem['start']
        # Fixed epsilon; per-entry decaying step size. Both supplied, not assessed.
        for _ in range(200):
            action = choose_action(q_values, state, actions(problem, state), .2, policy_rng)
            target, reward = sample_transition(problem, state, action, world_rng)
            key = (state, action)
            visits[key] = visits.get(key, 0) + 1
            alpha = 1 / visits[key] ** .6
            q_values = q_update(q_values, state, action, reward, target,
                                actions(problem, target), alpha, problem['discount'])
            state = target
            if state is None:
                completed += 1
                break
        # A 200-step cutoff is a reset, not an observed terminal transition.
    return q_values, completed


def filter_trace(problem, predict, observe, readings):
    belief = uniform_belief(problem)
    history = []
    for reading in readings:
        prior = predict(problem, belief)
        belief = observe(problem, prior, reading)
        history.append((prior, belief))
    return history


def particle_trace(problem, predict_particles, observe_particles, readings,
                   count=100, seed=0):
    rng = random.Random(seed)
    particles = initialise_particles(problem, count)
    history = []
    for reading in readings:
        particles = predict_particles(problem, particles, rng)
        prior = particle_belief(problem, particles)
        particles = observe_particles(problem, particles, reading, rng)
        history.append((prior, particle_belief(problem, particles)))
    return history


def total_variation(first, second):
    return .5 * sum(abs(first[s] - second[s]) for s in first)
