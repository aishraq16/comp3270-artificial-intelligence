"""Input, display and evaluation, without solutions to assessed game rules."""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
from support.constants import DIRECTIONS, WALL, PACMAN, FOOD, EMPTY
from support.maze_display import grid_lines
from support.terminal_output import prepare_maze_output


def load_case(question, name='corridor'):
    folder = ROOT / 'test_cases' / f'q{question}'
    name = name.replace('\\', '/')
    prefix = f'test_cases/q{question}/'
    if name.startswith('./'):
        name = name[2:]
    if name.startswith(prefix):
        name = name[len(prefix):]
    if '/' in name or name.endswith('_expected.json'):
        raise ValueError('Use a case name or a path shown by --list.')
    path = folder / (name if name.endswith('.json') else name + '.json')
    if not path.is_file():
        raise ValueError(f'Unknown Q{question} case: {name}. Use --list.')
    case = json.loads(path.read_text(encoding='utf-8'))
    return case, load_map(case['map'])


def load_map(name):
    if '/' in name or '\\' in name or not name.endswith('.json'):
        raise ValueError('Map must name a JSON file directly inside maps/.')
    data = json.loads((ROOT / 'maps' / name).read_text(encoding='utf-8'))
    grid = data['grid']
    if not grid or not grid[0] or any(len(row) != len(grid[0]) for row in grid):
        raise ValueError('Map rows must have one common nonzero width.')
    if any(c not in WALL + PACMAN + FOOD + EMPTY + 'WXYZ' for row in grid for c in row):
        raise ValueError('Map cells must use the A1 wall, Pacman, food and empty symbols, or W/X/Y/Z.')
    cells = [(r, c, ch) for r, row in enumerate(grid) for c, ch in enumerate(row)]
    starts = [(r, c) for r, c, ch in cells if ch == PACMAN]
    if len(starts) != 1:
        raise ValueError('Map must contain exactly one Pacman symbol.')
    ghosts = {ch: (r, c) for r, c, ch in cells if ch in 'WXYZ'}
    if len(ghosts) != sum(ch in 'WXYZ' for _, _, ch in cells) or not ghosts:
        raise ValueError('Maps need one to four uniquely labelled ghosts.')
    return {
        'grid': grid, 'walls': frozenset((r, c) for r, c, ch in cells if ch == WALL),
        'start': starts[0], 'ghosts': dict(sorted(ghosts.items())),
        'food': frozenset((r, c) for r, c, ch in cells if ch == FOOD),
        'map_file': 'maps/' + name,
    }


def initial_state(problem):
    return {'pos': problem['start'], 'ghosts': dict(problem['ghosts']),
            'food': problem['food'], 'score': 0,
            'winner': None if problem['food'] else 'Pacman'}


def state_from_json(raw):
    return {'pos': tuple(raw['pos']),
            'ghosts': {g: tuple(p) for g, p in raw['ghosts'].items()},
            'food': frozenset(tuple(p) for p in raw['food']),
            'score': raw['score'], 'winner': raw.get('winner')}


def state_to_json(state):
    return {'pos': list(state['pos']),
            'ghosts': {g: list(p) for g, p in sorted(state['ghosts'].items())},
            'food': [list(p) for p in sorted(state['food'])],
            'score': state['score'], 'winner': state['winner']}


def evaluate(problem, state):
    """Fixed leaf evaluator for Q5/Q6; terminal utility is the final score."""
    if state['winner'] is not None:
        return state['score']
    return state['score'] - 10 * len(state['food'])


def choose_reflex(problem, state, evaluator, successor, actions):
    """Supplied action selection; the assessed evaluation belongs in Q2/Q4."""
    choices = actions(problem, state, 'P')
    if not choices:
        choices = [None]
    best_action, best_value = None, -math.inf
    for action in choices:
        value = evaluator(problem, state, action)
        if type(value) not in (int, float) or not math.isfinite(value):
            raise ValueError('Evaluation must return a finite number.')
        if value > best_value:
            best_action, best_value = action, value
    return best_action


def render(problem, state):
    """Use A1's maze symbols and identical outside row/column labels."""
    prepare_maze_output()
    rows = []
    for r, row in enumerate(problem['grid']):
        chars = []
        for c in range(len(row)):
            pos = (r, c)
            ch = WALL if pos in problem['walls'] else FOOD if pos in state['food'] else EMPTY
            if pos == state['pos']:
                ch = PACMAN
            for ghost, ghost_pos in state['ghosts'].items():
                if pos == ghost_pos:
                    ch = ghost
            chars.append(ch)
        rows.append(''.join(chars))
    return '\n'.join([f"Map: {problem['map_file']}", *grid_lines(rows),
                      f"Score: {state['score']} | Food remaining: {len(state['food'])}"])
