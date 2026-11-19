"""Public fixture runner. Expected data are numerical, not formatted transcripts."""
import copy
import json
import math
import random
from pathlib import Path
from .models import load_problem, uniform_belief

CASES = Path(__file__).resolve().parents[1] / 'test_cases'


class RecordedRng:
    """Record public calls without changing Random's seeded choice behaviour."""
    def __init__(self, seed):
        self._random = random.Random(seed)
        self.calls = []

    def random(self):
        self.calls.append('random')
        return self._random.random()

    def choice(self, items):
        self.calls.append('choice')
        return self._random.choice(items)


def check_result_type(operation, result, problem, args):
    """Check Python representations before JSON display erases their types."""
    if operation in ('predict_particles', 'observe_particles'):
        if not isinstance(result, list) or len(result) != len(args[1]):
            raise AssertionError('Return a list with one entry per input particle')
        if any(not isinstance(s, tuple) or s not in problem['states'] for s in result):
            raise AssertionError('Each particle must be a valid (row, column) tuple, not a list')
    elif operation in ('value_iteration', 'predict', 'observe', 'q_update'):
        if not isinstance(result, dict):
            raise AssertionError('Return a dictionary')
        if operation != 'q_update' and result.keys() != set(problem['states']):
            raise AssertionError('Return exactly one dictionary entry per valid position')



def pack(value):
    if isinstance(value, dict):
        return {repr(k): pack(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [pack(v) for v in value]
    return value


def close(actual, expected):
    if isinstance(expected, dict):
        return (isinstance(actual, dict) and actual.keys() == expected.keys()
                and all(close(actual[k], v) for k, v in expected.items()))
    if isinstance(expected, list):
        return (isinstance(actual, list) and len(actual) == len(expected)
                and all(close(a, b) for a, b in zip(actual, expected)))
    if isinstance(expected, (int, float)) and not isinstance(expected, bool):
        return (isinstance(actual, (int, float)) and not isinstance(actual, bool)
                and math.isclose(actual, expected, rel_tol=1e-8, abs_tol=1e-9))
    return actual == expected


def run_case(api, case):
    """Return a JSON-friendly result and check nonmutation / fresh returns."""
    problem = load_problem(case['map'])
    operation = case['operation']
    rng = RecordedRng(case.get('seed', 0))
    if operation == 'value_iteration':
        args = [problem, case['iterations']]
    elif operation == 'action_value':
        values = {s: 0.0 for s in problem['states']}
        values.update({tuple(s): v for s, v in case.get('values', [])})
        args = [problem, tuple(case['state']), case['action'], values]
    elif operation in ('choose_action', 'q_update'):
        q_values = {(tuple(s), a): v for s, a, v in case.get('q_values', [])}
        state = tuple(case['state'])
        if operation == 'choose_action':
            args = [q_values, state, tuple(case['actions']), case['epsilon'], rng]
        else:
            target = None if case['next_state'] is None else tuple(case['next_state'])
            args = [q_values, state, case['action'], case['reward'], target,
                    tuple(case['next_actions']), case['alpha'], case['gamma']]
    elif operation in ('predict', 'observe'):
        belief = uniform_belief(problem)
        if 'belief' in case:
            belief = {s: 0.0 for s in problem['states']}
            belief.update({tuple(s): v for s, v in case['belief']})
        args = [problem, belief]
        if operation == 'observe':
            args.append(case['observation'])
    else:
        particles = [tuple(s) for s in case['particles']]
        args = [problem, particles]
        if operation == 'observe_particles':
            args.append(case['observation'])
        args.append(rng)
    before = copy.deepcopy([a for a in args if a is not rng])
    try:
        result = api[operation](*args)
    except ValueError:
        if case.get('raises') != 'ValueError':
            raise
        result = {'raises': 'ValueError'}
    else:
        if case.get('raises'):
            raise AssertionError('Expected ' + case['raises'])
        check_result_type(operation, result, problem, args)
        if operation not in ('choose_action', 'action_value'):
            if any(result is a for a in args):
                raise AssertionError('Return a fresh dictionary/list')
    if [a for a in args if a is not rng] != before:
        raise AssertionError('Input was modified')
    if 'rng_calls' in case and rng.calls != case['rng_calls']:
        raise AssertionError(f'RNG calls: expected {case["rng_calls"]!r}, got {rng.calls!r}')
    return pack(result)


def fixtures(question):
    return sorted(p for p in (CASES / f'q{question}').glob('*.json')
                  if not p.stem.endswith('_expected'))


def check(api, path):
    case = json.loads(path.read_text(encoding='utf8'))
    expected = json.loads(path.with_name(path.stem + '_expected.json').read_text(encoding='utf8'))
    case.update({key: expected[key] for key in ('raises', 'rng_calls') if key in expected})
    actual = run_case(api, case)
    if not close(actual, expected['result']):
        raise AssertionError(f'Expected {expected["result"]!r}\nActual   {actual!r}')
    return actual
