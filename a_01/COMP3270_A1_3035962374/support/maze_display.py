"""One compact monochrome maze display for play, previews and replays."""
from support.constants import WALL, PACMAN, FOOD, EMPTY
from support.terminal_output import prepare_maze_output


def grid_lines(grid):
    """Add identical outside coordinates to a one-character-per-cell grid."""
    columns = len(grid[0])
    prefix = len(str(len(grid) - 1)) + 1
    lines = []
    for place in reversed(range(len(str(columns - 1)))):
        labels = ''.join(str(c // (10 ** place) % 10) if c >= 10 ** place or place == 0 else ' '
                         for c in range(columns))
        lines.append(' ' * prefix + labels)
    lines.extend(f'{r:>{prefix - 1}} ' + row for r, row in enumerate(grid))
    return lines


def maze_lines(problem):
    """Keep one character per cell; put coordinates outside the JSON grid."""
    prepare_maze_output()
    rendered = []
    for r, row in enumerate(problem['grid']):
        text = ''
        for c, cell in enumerate(row):
            state = (r, c)
            symbol = EMPTY
            cost = problem.get('cell_costs', {}).get(state, 1)
            if cost != 1: symbol = str(cost)
            if state in problem['goal_states']: symbol = FOOD
            if state == problem['start_state']: symbol = PACMAN
            text += WALL if cell == WALL else symbol
        rendered.append(text)
    lines = [f"Map: {problem.get('map_file', '(in-memory maze)')}", *grid_lines(rendered)]
    # Preserve costs when Pacman covers a numbered cell during manual play.
    if problem.get('cell_costs'):
        lines.append('Entry costs: ' + ', '.join(f'{pos}={cost}' for pos, cost in sorted(problem['cell_costs'].items())))
    return lines
