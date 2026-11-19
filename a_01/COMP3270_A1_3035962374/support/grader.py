"""Supplied command options and public tests for Q0–Q4."""
import argparse
import json
from copy import deepcopy
from pathlib import Path
from support.problem import load_maze
from support.problem import is_goal
from support.constants import WALL
from support.file_names import input_name

CASES = Path(__file__).resolve().parents[1] / 'test_cases'


def student_frame(error):
    frame = None
    trace = error.__traceback__
    while trace is not None:
        code = trace.tb_frame.f_code
        name = Path(code.co_filename).name
        if name in {f'q{n}.py' for n in range(7)}:
            frame = (name, trace.tb_lineno, code.co_name)
        trace = trace.tb_next
    return frame


def error_detail(error):
    frame = student_frame(error)
    location = f'{frame[0]}:{frame[1]} in {frame[2]}\n' if frame else ''
    message = f'{location}{type(error).__name__}: {error}'
    if isinstance(error, NotImplementedError) and frame:
        message += f'\nComplete {frame[2]} in {frame[0]} first. Then run python3 {frame[0]} corridor --test.'
    return message


def unfinished_dependency(error, names):
    frame = student_frame(error)
    return isinstance(error, NotImplementedError) and frame is not None and frame[0] in names


def search_summary(result):
    path = result['path']
    print('No route found.' if path is None else 'Solution found.')
    if path is not None:
        print('Moves:', len(path) - 1)
    print('Expanded states:', len(result['expanded']))
    if 'cost' in result and path is not None:
        print('Total cost:', result['cost'])


def compare_result(actual, expected, display=repr):
    """Show one useful difference, even when a search returns thousands of states."""
    for key in ('expanded', 'path', 'cost'):
        if key not in expected or actual[key] == expected[key]:
            continue
        got, wanted = actual[key], expected[key]
        if isinstance(got, list) and isinstance(wanted, list):
            index = next((i for i, (a, b) in enumerate(zip(got, wanted)) if a != b), min(len(got), len(wanted)))
            expected_item = display(wanted[index]) if index < len(wanted) else '(end of list)'
            actual_item = display(got[index]) if index < len(got) else '(end of list)'
            detail = (f'First difference: {key}[{index}] (index starts at 0).\n'
                      f'Expected: {expected_item}\nActual:   {actual_item}\n'
                      f'{key} length: expected {len(wanted)}, actual {len(got)}.')
            if key == 'expanded':
                detail += '\nCheck goal-test timing, successor order and frontier ordering.'
        else:
            detail = f'First difference: {key}.\nExpected: {wanted!r}\nActual:   {got!r}'
        raise AssertionError(detail)


def parse_tests(names, args, allow_replay=False, question='Q2'):
    default_case = 'corridor'
    description = f'Run {default_case} by default; add --test to check.'
    visual_flag = '--show-maze' if question == 'Q1' else '--replay'
    epilog = f'With {visual_flag} and --test, select a named case.'
    if question != 'Q1':
        epilog += ' Redirected replay output prints all frames without prompts.'
    parser = argparse.ArgumentParser(description=description, allow_abbrev=False,
        epilog=epilog if allow_replay else None)
    folder = f'test_cases/{question.lower()}'
    parser.add_argument('case', nargs='?', choices=names, metavar='case',
                        type=lambda value: input_name(value, folder),
                        help=f'test case name, name.json or {folder}/name.json; use --list to see files')
    parser.add_argument('-l', '--list', action='store_true', help='list available test case files')
    parser.add_argument('-t', '--test', action='store_true', help='run public checks for all cases, or one named case')
    if allow_replay:
        if question in ('Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6'):
            parser.add_argument('-m' if question == 'Q1' else '-r', visual_flag, dest='visualize', action='store_true', help='add the maze display before calling your functions' if question == 'Q1' else 'add a step-by-step replay of your returned result')
    parser.set_defaults(visualize=False, test=False)
    options = parser.parse_args(args)
    if options.list and options.visualize:
        parser.error(f'--list cannot be combined with {visual_flag}.')
    if options.test and options.visualize and not options.case:
        parser.error(f'Select one test case when combining --test with {visual_flag}.')
    return options


def grade_q0(count_moves, args):
    folder = CASES / 'q0'
    available = {p.stem: p for p in sorted(folder.glob('*.json')) if not p.stem.endswith('_expected')}
    options = parse_tests(list(available), args, question='Q0')
    if options.list:
        print('Q0 available test case files:\n' + '\n'.join(f'test_cases/q0/{name}.json' for name in available))
        return 0
    if not options.test:
        name = options.case or 'corridor'
        case = json.loads(available[name].read_text(encoding='utf-8'))
        path = [tuple(state) for state in case['path']]
        from support.maze_display import maze_lines
        print(f'Running Q0: {name}')
        print('\n'.join(maze_lines(load_maze(available[name]))))
        print('Path:', path)
        try:
            print('Moves:', count_moves(path))
        except Exception as error:
            print(error_detail(error))
            return 1
        return 0
    cases = [available[options.case]] if options.case else list(available.values())
    passed = 0
    for file in cases:
        case = json.loads(file.read_text(encoding='utf-8'))
        try:
            actual = count_moves([tuple(state) for state in case['path']])
            if type(actual) is not int:
                raise ValueError('count_moves must return an integer.')
            wanted = json.loads(file.with_name(file.stem + '_expected.json').read_text(encoding='utf-8'))['moves']
            if actual != wanted:
                raise AssertionError(f"Expected: {wanted!r}\nActual:   {actual!r}")
            print(f'{file.stem}: PASSED')
            passed += 1
        except Exception as error:
            print(f'{file.stem}: FAILED\n{error_detail(error)}')
    return finish('Q0', passed, len(cases))


def validate_result(problem, result):
    import q1
    required = {'expanded', 'path', 'cost'} if 'cell_costs' in problem else {'expanded', 'path'}
    if not isinstance(result, dict) or set(result) != required:
        raise ValueError(f'Return a dict with exactly {sorted(required)}.')
    expanded, path = result['expanded'], result['path']
    if not isinstance(expanded, list):
        raise ValueError('expanded must be a list of (row, column) tuples.')
    if any(not replay_position(problem, state) for state in expanded):
        raise ValueError('Expanded states must be valid (row, column) tuples, e.g. (1, 2), not [1, 2].')
    if len(expanded) != len(set(expanded)):
        raise ValueError('expanded must not repeat states.')
    if any(is_goal(problem, state) for state in expanded):
        raise ValueError('expanded must not include any food cell.')
    if path is None:
        if 'cell_costs' in problem and result['cost'] is not None:
            raise ValueError('When path is None, cost must also be None.')
        return
    if not isinstance(path, list) or not path:
        raise ValueError('A successful path must be a nonempty list of whole states.')
    if any(not replay_position(problem, state) for state in path):
        raise ValueError('Path states must be valid (row, column) tuples.')
    if path[0] != problem['start_state'] or not is_goal(problem, path[-1]):
        raise ValueError('The path must start at Pacman and end at a food cell.')
    if any(is_goal(problem, state) for state in path[:-1]):
        raise ValueError('Stop at the first food reached; do not continue through food.')
    for source, target in zip(path, path[1:]):
        if target not in [child for _, child, _ in q1.successors(problem, source)]:
            raise ValueError(f'Illegal move: {source!r} -> {target!r}')
    if 'cell_costs' in problem:
        cost = sum(problem['cell_costs'].get(target, 1) for source, target in zip(path, path[1:]))
        if type(result['cost']) is not int or result['cost'] != cost:
            raise ValueError(f'Incorrect path cost: expected {cost}, got {result["cost"]!r}.')



def replay_position(problem, state):
    # Validate replay coordinates independently of unfinished student code.
    if not isinstance(state, tuple) or len(state) != 2 or any(type(n) is not int for n in state):
        return False
    r, c = state
    return 0 <= r < len(problem['grid']) and 0 <= c < len(problem['grid'][0]) and problem['grid'][r][c] != WALL


def check_positions(problem, expected, is_valid_position):
    for case in expected['valid_positions']:
        state = tuple(case['state'])
        original = deepcopy(problem)
        actual = is_valid_position(problem, state)
        if problem != original:
            raise ValueError('is_valid_position must not modify problem or its grid.')
        if actual is not case['valid']:
            raise AssertionError(f"State: {state!r}\nExpected: {case['valid']!r}\nActual:   {actual!r}")


def check_successors(problem, expected, successors):
    for case in expected['successors']:
        state = tuple(case['state'])
        original = deepcopy(problem)
        actual = successors(problem, state)
        if problem != original:
            raise ValueError('successors must not modify problem or its grid.')
        if not isinstance(actual, list) or any(
                type(item) is not tuple or len(item) != 3 or type(item[1]) is not tuple
                or len(item[1]) != 2 or any(type(n) is not int for n in item[1])
                or type(item[2]) is not int for item in actual):
            wanted = [(action, tuple(child), cost) for action, child, cost in case['successors']]
            raise ValueError(f'Return a list of (action, (row, column), integer_cost) tuples.\nExpected: {wanted!r}\nActual:   {actual!r}')
        wanted = [(action, tuple(child), cost) for action, child, cost in case['successors']]
        if actual != wanted:
            raise AssertionError(f'State: {state!r}\nExpected: {wanted!r}\nActual:   {actual!r}')


def record(case, name, status, detail=''):
    print(f'{case} {name}: {status}')
    if detail:
        print(detail)


def selected_cases(question, args):
    folder = CASES / question.lower()
    available = {p.stem: p for p in sorted(folder.glob('*.json')) if '_expected.' not in p.name}
    options = parse_tests(list(available), args, allow_replay=True, question=question)
    if options.list:
        print(f'{question} available test case files:\n' + '\n'.join(f'test_cases/{question.lower()}/{name}.json' for name in available))
        return [], options
    if not options.test:
        return [available[options.case or 'corridor']], options
    return ([available[options.case]] if options.case else list(available.values())), options


def run_example(question, path, options, is_valid_position=None, successors=None, search=None):
    """Run student code once. Expected answers are never loaded here."""
    print(f'Running {question}: {path.stem}')
    problem = result = None
    try:
        if question == 'Q4':
            from support.weighted_maze import load_weighted_case
            problem = load_weighted_case(path)
        else:
            problem = load_maze(path)
        if question == 'Q1':
            if options.visualize:
                from support.maze_display import maze_lines
                print('\n'.join(maze_lines(problem)))
            print('Start state:', problem['start_state'])
            print('Valid position:', is_valid_position(problem, problem['start_state']))
            print('Successors:', successors(problem, problem['start_state']))
        else:
            actual = search(problem)
            validate_result(problem, actual)
            result = actual
            search_summary(result)
            if result['path'] is not None:
                print('Path:', result['path'])
    except Exception as error:
        print(error_detail(error))
        if options.visualize and question != 'Q1' and problem is not None:
            from support.maze_display import maze_lines
            print('Maze preview only: complete or fix your search to replay it.')
            print('\n'.join(maze_lines(problem)))
        return 1
    if options.visualize and question != 'Q1':
        from support.run_maze import replay_search
        replay_search(problem, result)
    return 0


def finish(question, passed, total):
    print(f'{question}: {passed}/{total} public checks passed')
    if passed == total and total:
        print(f'All {question} tests passed.')
    return 0 if passed == total else 1


def grade_q1(is_valid_position, successors, args):
    cases, options = selected_cases('Q1', args)
    if not cases:
        return 0
    if not options.test:
        return run_example('Q1', cases[0], options, is_valid_position, successors)
    passed = 0
    for path in cases:
        expected = json.loads(path.with_name(path.stem + '_expected.json').read_text(encoding='utf-8'))
        problem = None
        try:
            problem = load_maze(path)
            if options.visualize:
                from support.maze_display import maze_lines
                print('\n'.join(maze_lines(problem)))
            check_positions(problem, expected, is_valid_position)
            record(path.stem, 'valid positions', 'PASSED')
            passed += 1
        except Exception as error:
            record(path.stem, 'valid positions', 'FAILED', error_detail(error))
            record(path.stem, 'successors', 'SKIPPED', 'Complete is_valid_position first.')
        else:
            try:
                check_successors(problem, expected, successors)
                record(path.stem, 'successors', 'PASSED')
                passed += 1
            except Exception as error:
                record(path.stem, 'successors', 'FAILED', error_detail(error))
    return finish('Q1', passed, 2 * len(cases))


def grade_search(search, args, question):
    import q1
    algorithm = {'Q2': 'BFS', 'Q3': 'DFS', 'Q4': 'UCS'}[question]
    cases, options = selected_cases(question, args)
    if not cases:
        return 0
    if not options.test:
        return run_example(question, cases[0], options, search=search)
    passed = 0
    for path in cases:
        expected = json.loads(path.with_name(path.stem + '_expected.json').read_text(encoding='utf-8'))
        expected_result = expected['result']
        expected_q1 = expected['representation']
        problem = result = None
        try:
            if question == 'Q4':
                from support.weighted_maze import load_weighted_case
                problem = load_weighted_case(path)
            else:
                problem = load_maze(path)
            check_positions(problem, expected_q1, q1.is_valid_position)
            check_successors(problem, expected_q1, q1.successors)
        except Exception as error:
            record(path.stem, algorithm, 'SKIPPED',
                   f'Q1 prerequisite failed on this maze. Check your Q1 functions and run python3 q1.py --test.\n{error_detail(error)}')
            if unfinished_dependency(error, {'q1.py'}) and not options.visualize:
                remaining = len(cases) - cases.index(path) - 1
                if remaining:
                    print(f'Remaining {remaining} cases: SKIPPED until Q1 is implemented.')
                break
        else:
            try:
                actual = search(problem)
                validate_result(problem, actual)
                result = actual
                print(f'Checking {question}: {path.stem}')
                search_summary(actual)
                wanted = {key: ([tuple(state) for state in value] if key in ('expanded', 'path') and value is not None else value)
                          for key, value in expected_result.items()}
                compare_result(actual, wanted)
                record(path.stem, algorithm, 'PASSED')
                passed += 1
            except Exception as error:
                record(path.stem, algorithm, 'FAILED', error_detail(error))
        if options.visualize:
            if result is None:
                print('Maze preview only: fix the reported error and run again.')
                if problem is not None:
                    from support.maze_display import maze_lines
                    print('\n'.join(maze_lines(problem)))
            else:
                from support.run_maze import replay_search
                replay_search(problem, result)
    return finish(question, passed, len(cases))


def grade_q2(search, args):
    return grade_search(search, args, 'Q2')


def grade_q3(search, args):
    return grade_search(search, args, 'Q3')


def grade_q4(search, args):
    return grade_search(search, args, 'Q4')
