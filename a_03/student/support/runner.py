"""Shared named-case command line, matching the A1/A2 workflow."""
import argparse
import json
from pathlib import Path
from .checks import fixtures, check, run_case
from .models import load_problem
from .display import show_map


def main(question, api):
    parser = argparse.ArgumentParser(description=f'COMP3270 A3 Q{question}')
    parser.add_argument('case', nargs='?', help='case name, name.json or test_cases/qN/name.json')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-l', '--list', action='store_true')
    group.add_argument('-t', '--test', action='store_true')
    group.add_argument('--inspect', action='store_true')
    group.add_argument('-m', '--show-maze', action='store_true')
    args = parser.parse_args()
    paths = {p.stem: p for p in fixtures(question)}
    if args.list:
        for name, path in paths.items():
            case = json.loads(path.read_text(encoding='utf8'))
            print(f'{name}: {case["description"]}')
        return
    name = Path(args.case).stem if args.case else ('all' if args.test else None)
    if name is None:
        if args.inspect or args.show_maze:
            parser.error('Select one case. Use --list to see names.')
        parser.print_help()
        return
    if name != 'all' and name not in paths:
        parser.error('Unknown case. Use --list to see names.')
    if args.test:
        selected = paths.items() if name == 'all' else [(name, paths[name])]
        failures = 0
        for label, path in selected:
            try:
                check(api, path)
                print(f'{label}: PASSED')
            except Exception as error:
                failures += 1
                print(f'{label}: FAILED\n{type(error).__name__}: {error}')
        print(f'{len(selected) - failures}/{len(selected)} passed')
        if failures:
            raise SystemExit(1)
        return
    if name == 'all':
        parser.error('Select one case for --inspect or --show-maze')
    case = json.loads(paths[name].read_text(encoding='utf8'))
    show_map(load_problem(case['map']))
    if args.inspect or not args.show_maze:
        print('Case inputs:')
        print(json.dumps(case, indent=2))
        try:
            print('Your result:')
            print(json.dumps(run_case(api, case), indent=2))
        except Exception as error:
            parser.exit(1, f'{type(error).__name__}: {error}\n')
