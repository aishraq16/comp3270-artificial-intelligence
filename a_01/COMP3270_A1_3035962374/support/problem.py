"""Supplied grid loading and goal checking. No changes needed."""
import json
from pathlib import Path
from support.constants import WALL, PACMAN, FOOD, EMPTY


def is_goal(problem, state):
    return state in problem['goal_states']


def make_problem(data, weighted=False):
    """Infer the start and food positions from the grid; normalize cost cells."""
    if any(key in data for key in ('start', 'goal', 'edges')):
        raise ValueError('Put the start, food and costs in the grid, not in separate fields.')
    grid = data['grid']
    if not grid or any(not isinstance(row, str) or not row for row in grid) or len({len(row) for row in grid}) != 1:
        raise ValueError('The maze must be a nonempty rectangle.')
    allowed = (WALL, PACMAN, FOOD, EMPTY, '3', '5') if weighted else (WALL, PACMAN, FOOD, EMPTY)
    if any(cell not in allowed for row in grid for cell in row):
        raise ValueError('Use the supplied maze symbols' + (' and 3 or 5 for cell-entry costs.' if weighted else '.'))
    starts = [(r, c) for r, row in enumerate(grid) for c, cell in enumerate(row) if cell == PACMAN]
    goals = [(r, c) for r, row in enumerate(grid) for c, cell in enumerate(row) if cell == FOOD]
    if len(starts) != 1 or not goals:
        raise ValueError('The grid must contain exactly one Pacman (●) and at least one food (·), in separate cells.')
    problem = {
        'grid': [''.join(EMPTY if cell in '35' else cell for cell in row) for row in grid],
        'start_state': starts[0],
        'goal_states': goals,
        'title': data.get('title', 'Pacman maze'),
    }
    if 'map_file' in data:
        problem['map_file'] = data['map_file']
    if weighted:
        problem['cell_costs'] = {(r, c): int(cell) for r, row in enumerate(grid) for c, cell in enumerate(row) if cell in '35'}
    return problem


MAPS = Path(__file__).resolve().parents[1] / 'maps'


def load_data(path):
    """Read a map or resolve a test case's reference to a shared map."""
    path = Path(path)
    data = json.loads(path.read_text(encoding='utf-8'))
    if 'map' in data:
        name = data['map']
        if not isinstance(name, str) or Path(name).name != name or not name.endswith('.json'):
            raise ValueError('A map reference must be a filename inside maps/.')
        if 'grid' in data:
            raise ValueError('A test case references a map; it must not repeat the grid.')
        maze = json.loads((MAPS / name).read_text(encoding='utf-8'))
        data = {**maze, **data, 'map_file': 'maps/' + name}
    else:
        data['map_file'] = 'maps/' + path.name if path.parent.resolve() == MAPS.resolve() else path.name
    return data


def load_maze(path, weighted=False):
    return make_problem(load_data(path), weighted=weighted)
