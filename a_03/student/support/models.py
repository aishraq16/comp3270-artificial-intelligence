"""Supplied environments. Positions are (row, column), starting at zero."""
import json
from pathlib import Path
from collections import Counter

DIRECTIONS = (('North', (-1, 0)), ('East', (0, 1)),
              ('South', (1, 0)), ('West', (0, -1)))
ACTION_ORDER = tuple(name for name, _ in DIRECTIONS)
ROOT = Path(__file__).resolve().parents[1]


def load_problem(name):
    """Load a named supplied map, without any changing simulation state."""
    path = ROOT / 'maps' / (name if name.endswith('.json') else name + '.json')
    raw = json.loads(path.read_text(encoding='utf8'))
    grid = raw['grid']
    if not grid or any(len(row) != len(grid[0]) for row in grid):
        raise ValueError('Grid must be nonempty and rectangular')
    states = tuple((r, c) for r, row in enumerate(grid)
                   for c, symbol in enumerate(row) if symbol != '█')
    starts = [(r, c) for r, row in enumerate(grid)
              for c, symbol in enumerate(row) if symbol == '●']
    if len(starts) != 1:
        raise ValueError('Each map needs exactly one ● marker')
    problem = dict(raw, states=states, walls=frozenset(
        (r, c) for r, row in enumerate(grid) for c, symbol in enumerate(row)
        if symbol == '█'), start=starts[0], map_file=path.name)
    problem['exits'] = {tuple(item['position']): item['reward']
                        for item in raw.get('exits', [])}
    return problem


def moved(problem, state, direction):
    dr, dc = dict(DIRECTIONS)[direction]
    target = (state[0] + dr, state[1] + dc)
    return target if target in problem['states'] else state


def actions(problem, state):
    """Exit cells allow only Exit; blocked movement remains a valid action."""
    if state is None:
        return ()
    return ('Exit',) if state in problem['exits'] else ACTION_ORDER


def transitions(problem, state, action):
    """Return (probability, next_state, reward) tuples, combining duplicates."""
    if action not in actions(problem, state):
        raise ValueError('Action is not available in this state')
    if action == 'Exit':
        return ((1.0, None, problem['exits'][state]),)
    index = ACTION_ORDER.index(action)
    noise = problem['noise']
    mass = {}
    for offset, probability in ((0, 1 - 2 * noise), (-1, noise), (1, noise)):
        if probability:
            target = moved(problem, state, ACTION_ORDER[(index + offset) % 4])
            mass[target] = mass.get(target, 0.0) + probability
    return tuple((mass[target], target, problem['living_reward'])
                 for target in sorted(mass))


def sample_distribution(weights, rng):
    """Sample one key using one rng.random() call; tuple keys sorted row-major.

    Weights may be unnormalised. Zero weights are never selected.
    Reject negative, nonfinite or all-zero weights.
    """
    import math
    if any(not math.isfinite(w) or w < 0 for w in weights.values()):
        raise ValueError('Weights must be finite and nonnegative')
    total = sum(weights.values())
    if total <= 0:
        raise ValueError('Cannot sample zero total weight')
    threshold = rng.random() * total
    cumulative = 0.0
    last = None
    for key in sorted(weights):
        if weights[key] > 0:
            last = key
            cumulative += weights[key]
            if threshold < cumulative:
                return key
    return last  # Floating-point roundoff at the upper endpoint.


def sample_transition(problem, state, action, rng):
    outcomes = transitions(problem, state, action)
    # An index distribution also handles the terminal state None.
    index = sample_distribution({i: item[0] for i, item in enumerate(outcomes)}, rng)
    _, target, reward = outcomes[index]
    return target, reward


def ghost_transitions(problem, state):
    """Direction probabilities come from the map; default .25 each.

    Return a sparse dictionary {next_position: probability}. Blocked moves stay.
    """
    result = {}
    probabilities = problem.get('direction_probabilities',
                                {a: .25 for a in ACTION_ORDER})
    for direction in ACTION_ORDER:
        probability = probabilities[direction]
        if probability:
            target = moved(problem, state, direction)
            result[target] = result.get(target, 0.0) + probability
    return result


def observation_probability(problem, state, observation):
    """P(reading | ghost position), supplied rather than implemented by students.

    Reading = max(0, Manhattan distance to ● + error).
    Error -1, 0, +1 has probability .2, .6, .2 respectively.
    The observer stays fixed; walls do not change Manhattan distance.
    """
    r, c = problem['start']
    distance = abs(state[0] - r) + abs(state[1] - c)
    return sum(p for error, p in ((-1, .2), (0, .6), (1, .2))
               if max(0, distance + error) == observation)


def uniform_belief(problem):
    return {s: 1 / len(problem['states']) for s in problem['states']}


def initialise_particles(problem, count):
    """Cycle row-major states. Counts differ by at most one. Uses no RNG."""
    if count < 1:
        raise ValueError('Particle count must be positive')
    states = problem['states']
    return [states[i % len(states)] for i in range(count)]


def particle_belief(problem, particles):
    counts = Counter(particles)
    return {s: counts[s] / len(particles) for s in problem['states']}
