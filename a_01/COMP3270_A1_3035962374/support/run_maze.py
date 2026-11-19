"""Supplied Q1–Q4 maze display and replay."""
import shutil
import sys
from support.constants import PACMAN, FOOD, WALL, EMPTY
from support.maze_display import maze_lines, grid_lines
from support.grader import validate_result


def print_coordinates(label, states, brackets):
    """Wrap long collections between coordinates, preserving their order."""
    if not states and brackets == '{}':
        print(label + 'set()')
        return
    width = max(24, shutil.get_terminal_size((80, 24)).columns)
    line = label + brackets[0]
    for index, state in enumerate(states):
        item = str(state) + (', ' if index < len(states) - 1 else '')
        if len(line) + len(item) + 1 > width:
            print(line.rstrip())
            line = '  '
        line += item
    print(line + brackets[1])


def replay_lines(problem, expanded, current=None, path=None, complete=False):
    """Separate immutable maze contents from search status and final route."""
    original = maze_lines(problem)
    height = len(problem['grid']) + len(str(len(problem['grid'][0]) - 1))
    left = ['Maze (unchanged)', *original[1:1 + height]]
    title = 'Returned path' if complete and path is not None else 'Search progress'
    if complete and path is None:
        title = 'No path found'
    visited, route = set(expanded), set(path or [])
    progress = []
    for r, row in enumerate(problem['grid']):
        text = ''
        for c, cell in enumerate(row):
            state = (r, c)
            symbol = EMPTY
            if complete and path is not None:
                if state in route: symbol = '○'
            else:
                if state in visited: symbol = '░'
                if state == current: symbol = '◎'
            text += WALL if cell == WALL else symbol
        progress.append(text)
    right = [title, *grid_lines(progress)]
    left_width = max(map(len, left))
    right_width = max(len('Search progress'), *map(len, right))
    width = shutil.get_terminal_size((80, 24)).columns
    lines = [original[0]]
    if left_width + 4 + right_width <= width:
        lines.extend((a.ljust(left_width) + '    ' + z).rstrip() for a, z in zip(left, right))
    else:
        lines.extend([*left, '', *right])
    lines.extend(original[1 + height:])
    return lines


def replay_search(problem, result):
    validate_result(problem, result)
    interactive = sys.stdin.isatty() and sys.stdout.isatty()
    expanded = result['expanded']
    for step in range(len(expanded) + 2):
        done = step > len(expanded)
        count = min(step, len(expanded))
        current = expanded[step - 1] if 0 < step <= len(expanded) else None
        if interactive:
            print('\033[2J\033[H', end='')
        print(problem['title'])
        print('\n'.join(replay_lines(problem, expanded[:count], current, result['path'], done)))
        print(f'{PACMAN} Start   {FOOD} Food   (unchanged maze)')
        if done and result['path'] is not None:
            print('○ Returned path, including start and goal')
        else:
            print('░ Expanded earlier   ◎ Just expanded')
        if 'cell_costs' in problem:
            print('Pay the destination cell’s number when entering it; unnumbered cells cost 1. Start at cost 0.')
        print('Search replay: expansion order, not Pacman movement. Maze stays unchanged.')
        print(f'Expanded so far: {count} / {len(expanded)}')
        if not done:
            print(f'Just expanded: {current if current is not None else "none (initial state)"}')
        print_coordinates('Explored set: ', sorted(set(expanded[:count])), '{}')
        if done:
            print('Search complete.')
            if 'cost' in result:
                print('Total cost:', result['cost'])
            if result['path'] is None:
                print('Search returned no path')
            else:
                print(f"Returned path: {len(result['path']) - 1} moves")
                print_coordinates('Path (start to goal): ', result['path'], '[]')
        if interactive and not done:
            try:
                command = input('Enter: next step; q: quit > ').strip().lower()
            except (EOFError, KeyboardInterrupt):
                print()
                return
            if command == 'q':
                return
