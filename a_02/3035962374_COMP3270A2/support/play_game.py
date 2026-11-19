"""Manual Pacman using the student's Q1 rules, after completing Q1."""
import argparse
import os
import random
import sys

from support.game import ROOT, initial_state, load_map, render
from support.terminal_output import prepare_maze_output

NAMES = tuple(path.stem for path in sorted((ROOT / 'maps').glob('*.json')))
DIRECTIONS = {'w': 'North', 'a': 'West', 's': 'South', 'd': 'East'}


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


def map_name(value):
    """Accept a shared map's stem, filename or relative maps/ filename."""
    name = value.replace('\\', '/')
    if name.startswith('./'):
        name = name[2:]
    if name.startswith('maps/'):
        name = name[5:]
    if '/' in name:
        raise argparse.ArgumentTypeError('Use a map name or a path shown by --list.')
    return name[:-5] if name.endswith('.json') else name


def frame(problem, state, turns, notice, interactive):
    lines = ['Pacman | Manual play', render(problem, state),
             f'Pacman turns: {turns}']
    if state['winner'] is not None:
        lines += [f'Winner: {state["winner"]}', 'R: play again   Q: quit']
    else:
        lines += [notice or 'Eat every food dot and avoid the ghosts.',
                  'Arrow keys / WASD: move   R: restart   Q: quit' if interactive
                  else 'W/A/S/D + Enter: move   R: restart   Q: quit']
    print(('\033[H' + '\033[K\n'.join(lines) + '\033[K\033[J')
          if interactive else '\n'.join(lines), flush=True)


def main(args=None):
    parser = argparse.ArgumentParser(
        description='Move Pacman yourself using your completed Q1 game rules.',
        allow_abbrev=False)
    parser.add_argument('case', nargs='?', default='crossroads', type=map_name,
                        choices=NAMES, metavar='map',
                        help='map name, name.json or maps/name.json; default: crossroads')
    parser.add_argument('-l', '--list', action='store_true', help='list shared map files')
    parser.add_argument('--seed', type=int, default=8, help='ghost random seed; default: 8')
    options = parser.parse_args(args)
    if options.list:
        print('\n'.join('maps/' + name + '.json' for name in NAMES))
        return 0
    prepare_maze_output()
    interactive = sys.stdin.isatty() and sys.stdout.isatty()
    old_settings = None
    try:
        from q1 import legal_actions, successor, random_action
        problem = load_map(options.case + '.json')
        state, rng = initial_state(problem), random.Random(options.seed)
        turns, notice = 0, ''
        try:
            if interactive:
                if os.name != 'nt':
                    import termios
                    import tty
                    old_settings = termios.tcgetattr(sys.stdin)
                    tty.setcbreak(sys.stdin.fileno())
                print('\033[?1049h\033[?25l', end='', flush=True)
            while True:
                frame(problem, state, turns, notice, interactive)
                command = read_key(interactive)
                if command == 'q':
                    break
                if command == 'r':
                    state, rng = initial_state(problem), random.Random(options.seed)
                    turns, notice = 0, ''
                    continue
                if command in ('\r', '\n', ''):
                    continue
                if state['winner'] is not None:
                    continue
                if command not in DIRECTIONS:
                    notice = ('Use arrow keys or W/A/S/D to move.' if interactive
                              else 'Enter one of W, A, S, D, R, or Q.')
                    continue
                moves = legal_actions(problem, state, 'P')
                action = DIRECTIONS[command] if moves else None
                if moves and action not in moves:
                    notice = 'Blocked: choose another direction. Turn count unchanged.'
                    continue
                state = successor(problem, state, 'P', action)
                turns += 1
                notice = ('Pacman has no legal move: forced pass (-1 point).'
                          if action is None else '')
                for ghost in sorted(problem['ghosts']):
                    if state['winner'] is not None:
                        break
                    state = successor(problem, state, ghost,
                                      random_action(problem, state, ghost, rng))
        except (EOFError, KeyboardInterrupt):
            pass
        finally:
            if interactive:
                try:
                    print('\033[0m\033[?25h\033[?1049l', end='', flush=True)
                finally:
                    if old_settings is not None:
                        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    except Exception as error:
        from support.runner import error_detail
        print(error_detail(error), file=sys.stderr)
        return 1
    print('Game ended.')
    return 0
