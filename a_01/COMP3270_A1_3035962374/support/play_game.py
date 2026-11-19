"""Manual play, independent of every student implementation."""
import argparse
import os
from pathlib import Path
import sys
from support.problem import load_maze, MAPS
from support.constants import WALL
from support.maze_display import maze_lines
from support.file_names import input_name

CASES = MAPS
NAMES = tuple(path.stem for path in sorted(MAPS.glob('*.json')))
DIRECTIONS = {'w': (-1, 0), 'a': (0, -1), 's': (1, 0), 'd': (0, 1)}


def read_key(interactive):
    if not interactive:
        line = sys.stdin.readline()
        return line.strip().lower() if line else 'q'
    if os.name == 'nt':
        import msvcrt
        key = msvcrt.getwch()
        if key in ('\x00', '\xe0'):
            return {'H': 'w', 'P': 's', 'K': 'a', 'M': 'd'}.get(msvcrt.getwch(), '')
    else:
        import select
        key = os.read(sys.stdin.fileno(), 1).decode('ascii', errors='ignore')
        if key == '\x1b':
            sequence = ''
            for _ in range(8):
                if not select.select([sys.stdin], [], [], .08)[0]:
                    break
                sequence += os.read(sys.stdin.fileno(), 1).decode('ascii', errors='ignore')
                if len(sequence) > 1 and sequence[-1].isalpha():
                    break
            return {'[A': 'w', '[B': 's', '[D': 'a', '[C': 'd',
                    'OA': 'w', 'OB': 's', 'OD': 'a', 'OC': 'd'}.get(sequence, '')
    return 'q' if key in ('\x03', '\x04', '') else key.lower()


def frame(problem, position, food, moves, notice, interactive, cost=0, goal='all'):
    lines = [f'Pacman | {problem["title"]}']
    display = dict(problem, start_state=position, goal_states=food)
    lines.extend(maze_lines(display))
    lines.append(f'Moves: {moves} | Food remaining: {len(food)}')
    won = not food if goal == 'all' else len(food) < len(problem['goal_states'])
    if problem.get('cell_costs'):
        lines.append(f'Total cost: {cost} (pay the destination cell; unnumbered cells cost 1)')
    if won:
        lines += [f'All food eaten in {moves} moves!' if goal == 'all' else f'Food reached in {moves} moves!',
                  'R: play again   Q: quit']
    else:
        lines += [notice or ('Eat every food dot.' if goal == 'all' else 'Reach any food dot.'),
                  'Arrow keys / WASD: move   R: restart   Q: quit' if interactive else 'W/A/S/D + Enter: move   R: restart   Q: quit']
    # Redraw from the same origin without clearing/flashing the whole screen.
    print(('\033[H' + '\033[K\n'.join(lines) + '\033[K\033[J') if interactive else '\n'.join(lines), flush=True)


def map_name(value):
    """Accept the stem or the relative filename printed by --list."""
    return input_name(value, 'maps')


def main(args=None):
    parser = argparse.ArgumentParser(description='Move Pacman yourself through a maze from any shared map file. No coding required.', allow_abbrev=False)
    parser.add_argument('case', nargs='?', default='playground', type=map_name, choices=NAMES, metavar='map', help='map name, name.json or maps/name.json; default: playground')
    parser.add_argument('-l', '--list', action='store_true', help='list shared map files')
    parser.add_argument('-g', '--goal', choices=('any', 'all'), default='all',
                        help='any: reach one food (Q1–Q4); all: collect all food (Q5/Q6, default)')
    options = parser.parse_args(args)
    if options.list:
        print('\n'.join('maps/' + name + '.json' for name in NAMES))
        return 0
    problem = load_maze(CASES / (options.case + '.json'), weighted=True)
    position, food, moves, notice = problem['start_state'], set(problem['goal_states']), 0, ''
    cost = 0
    interactive = sys.stdin.isatty() and sys.stdout.isatty()
    old_settings = None
    try:
        if interactive:
            if os.name != 'nt':
                import termios
                import tty
                old_settings = termios.tcgetattr(sys.stdin)
                tty.setcbreak(sys.stdin.fileno())
            print('\033[?1049h\033[?25l', end='', flush=True)
        while True:
            frame(problem, position, food, moves, notice, interactive, cost, options.goal)
            won = not food if options.goal == 'all' else len(food) < len(problem['goal_states'])
            if won and not interactive:
                return 0
            command = read_key(interactive)
            if command == 'q':
                break
            if command == 'r':
                position, food, moves, notice = problem['start_state'], set(problem['goal_states']), 0, ''
                cost = 0
                continue
            if command in ('\r', '\n', ''):
                continue
            if won:
                continue
            if command not in DIRECTIONS:
                notice = 'Use arrow keys or W/A/S/D to move.' if interactive else 'Enter one of W, A, S, D, R, or Q.'
                continue
            dr, dc = DIRECTIONS[command]
            destination = position[0] + dr, position[1] + dc
            r, c = destination
            if not (0 <= r < len(problem['grid']) and 0 <= c < len(problem['grid'][0])) or problem['grid'][r][c] == WALL:
                notice = 'Blocked: choose another direction. Move count unchanged.'
                continue
            position = destination
            moves += 1
            cost += problem.get('cell_costs', {}).get(position, 1)
            food.discard(position)
            notice = ''
    except (EOFError, KeyboardInterrupt):
        pass
    finally:
        if interactive:
            print('\033[0m\033[?25h\033[?1049l', end='', flush=True)
            if old_settings is not None:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    print('Game ended.')
    return 0
