"""Supplied representation-independent Q5/Q6 checks and path replay."""
from collections import deque
from copy import deepcopy
import json
from pathlib import Path
import sys
from support.problem import load_maze
from support.grader import parse_tests, finish, error_detail, unfinished_dependency, search_summary, compare_result
from support.maze_display import maze_lines

CASES = Path(__file__).resolve().parents[1] / 'test_cases/q5'


def load_problem(path):
    problem = load_maze(path)
    problem['pacman_start'] = problem.pop('start_state')
    problem['food_positions'] = tuple(problem.pop('goal_states'))
    return problem


def describe(api, state):
    position, food = api.pacman_position(state), api.remaining_food(state)
    def coordinate(value):
        return type(value) is tuple and len(value) == 2 and all(type(n) is int for n in value)
    if not coordinate(position):
        raise ValueError('pacman_position must return a (row, column) tuple.')
    if type(food) is not tuple:
        raise ValueError(f'remaining_food must return a tuple of coordinate tuples, not {type(food).__name__}.')
    if not all(coordinate(p) for p in food):
        raise ValueError('Each item returned by remaining_food must be a (row, column) tuple of integers.')
    if food != tuple(sorted(set(food))):
        raise ValueError('remaining_food must return distinct coordinate tuples, sorted by row then column.')
    try:
        hash(state)
    except TypeError:
        raise ValueError('Your state must work in an explored set; use an immutable, hashable representation.') from None
    return position, food


def legal_moves(problem, position):
    r, c = position
    grid = problem['grid']
    for action, dr, dc in [('North', -1, 0), ('East', 0, 1), ('South', 1, 0), ('West', 0, -1)]:
        child = r + dr, c + dc
        if 0 <= child[0] < len(grid) and 0 <= child[1] < len(grid[0]) and grid[child[0]][child[1]] != '█':
            yield action, child



def check_definition(api, problem, check_heuristic=False, expected_heuristics=None):
    """Check transitions and equivalent states independently of student BFS."""
    original_problem = deepcopy(problem)
    start = api.initial_state(problem)
    wanted = problem['pacman_start'], problem['food_positions']
    if describe(api, start) != wanted:
        raise ValueError('Initial state must contain Pacman and all food.')
    if api.initial_state(problem) != start:
        raise ValueError('Equivalent initial states must compare equal.')
    queue, representatives = deque([start]), {wanted: start}
    state_meanings = {start: wanted}
    while queue:
        state = queue.popleft()
        semantic = describe(api, state)
        position, food = semantic
        old_hash = hash(state)
        if check_heuristic:
            wanted_h = expected_heuristics[semantic]
            actual_h = api.heuristic(problem, state)
            if type(actual_h) is not int or actual_h != wanted_h:
                raise ValueError(f'Heuristic at {semantic!r}: expected {wanted_h}, got {actual_h!r}.')
            if describe(api, state) != semantic or hash(state) != old_hash:
                raise ValueError('heuristic must not modify the state.')
        if api.is_goal(problem, state) is not (not food):
            raise ValueError('is_goal must return True exactly when no food remains.')
        if describe(api, state) != semantic or hash(state) != old_hash:
            raise ValueError('is_goal must not modify the state.')
        if not food:
            continue
        actual = api.successors(problem, state)
        if not isinstance(actual, list):
            raise ValueError('successors must return a list of (action, child_state, 1) tuples.')
        wanted = [(action, (child, tuple(p for p in food if p != child)), 1)
                  for action, child in legal_moves(problem, position)]
        observed = []
        for item in actual:
            if type(item) is not tuple or len(item) != 3 or type(item[2]) is not int:
                raise ValueError('Each successor must be an (action, child_state, 1) tuple.')
            action, child, cost = item
            meaning = describe(api, child)
            if child in state_meanings and state_meanings[child] != meaning:
                raise ValueError("Different positions or remaining food must be different states.")
            state_meanings[child] = meaning
            observed.append((action, meaning, cost))
            if meaning in representatives:
                previous = representatives[meaning]
                if child != previous or hash(child) != hash(previous):
                    raise ValueError('Same position and remaining food must compare equal, regardless of history.')
            else:
                representatives[meaning] = child
                queue.append(child)
        if observed != wanted:
            raise ValueError(f'Incorrect successors at {semantic!r}. Expected {wanted!r}; got {observed!r}.')
        if describe(api, state) != semantic or hash(state) != old_hash:
            raise ValueError('Generating successors must not modify the parent state.')
    if problem != original_problem:
        raise ValueError('Problem functions and heuristic must not modify problem or its grid.')
    return len(representatives)


def validate_result(api, problem, result):
    """Check a usable returned path without reading expected answers or solving the maze."""
    if not isinstance(result, dict) or set(result) != {'expanded', 'path'}:
        raise ValueError('Return exactly expanded and path, as in Q2.')
    if type(result['expanded']) is not list or (result['path'] is not None and type(result['path']) is not list):
        raise ValueError('expanded and a successful path must be lists.')
    observed = {key: None if value is None else [describe(api, state) for state in value]
                for key, value in result.items()}
    grid = problem['grid']
    for states in observed.values():
        for (r, c), food in states or []:
            if not (0 <= r < len(grid) and 0 <= c < len(grid[0])) or grid[r][c] == '█':
                raise ValueError('Returned states must place Pacman in a traversable cell.')
            if not set(food) <= set(problem['food_positions']):
                raise ValueError('Remaining food must come from the original food positions.')
    expanded = observed['expanded']
    if len(expanded) != len(set(expanded)) or any(not food for _, food in expanded):
        raise ValueError('expanded must exclude duplicate states and all-food goals.')
    path = observed['path']
    if path is not None:
        if not path or path[0] != (problem['pacman_start'], problem['food_positions']):
            raise ValueError('The path must begin with Pacman and all original food.')
        if path[-1][1]:
            raise ValueError('A successful path must finish with no remaining food.')
        for (position, food), (child, remaining) in zip(path, path[1:]):
            if not food:
                raise ValueError('Stop when all food has been eaten.')
            if child not in [target for _, target in legal_moves(problem, position)]:
                raise ValueError('The path contains an illegal move.')
            if remaining != tuple(p for p in food if p != child):
                raise ValueError('Food must disappear exactly when Pacman enters its cell.')
    return observed


def replay(api, problem, result):
    path = result['path']
    if path is None:
        display = dict(problem, start_state=problem['pacman_start'], goal_states=problem['food_positions'])
        print(problem['title'])
        print('\n'.join(maze_lines(display)))
        print('Expanded states:', len(result['expanded']))
        print('No route collects all food.')
        return
    interactive = sys.stdin.isatty() and sys.stdout.isatty()
    for step, state in enumerate(path):
        position, food = describe(api, state)
        if interactive:
            print('\033[2J\033[H', end='')
        display = dict(problem, start_state=position, goal_states=food)
        print(problem['title'])
        print('\n'.join(maze_lines(display)))
        print(f'Move {step}/{len(path)-1} | Pacman: {position} | Food remaining: {len(food)}')
        print('Expanded states:', len(result['expanded']))
        if interactive and step < len(path)-1:
            try:
                command = input('Enter: next move; q: quit > ').strip().lower()
            except (EOFError, KeyboardInterrupt):
                print()
                return
            if command == 'q':
                return


def run(api, args, question='Q5'):
    folder = CASES.parent / question.lower()
    search = api.bfs_gsa if question == 'Q5' else api.a_star_gsa
    algorithm = 'BFS-GSA' if question == 'Q5' else 'A*-GSA'
    available = {p.stem: p for p in sorted(folder.glob('*.json')) if not p.stem.endswith('_expected')}
    options = parse_tests(list(available), args, allow_replay=True, question=question)
    if options.list:
        print(question + ' available test case files:\n' + '\n'.join(f'test_cases/{question.lower()}/{name}.json' for name in available))
        return 0
    names = [options.case or 'corridor'] if not options.test else ([options.case] if options.case else list(available))
    passed = 0
    for name in names:
        problem = load_problem(available[name])
        preview_problem = deepcopy(problem)
        original = repr(problem)
        result = None
        phase = 'problem definition' if question == 'Q5' else 'problem definition / heuristic'
        stop = False
        try:
            if options.test:
                expected_heuristics = None
                if question == 'Q6':
                    answers = json.loads(available[name].with_name(name + '_expected.json').read_text(encoding='utf-8'))
                    expected_heuristics = {
                        (tuple(item['state'][0]), tuple(tuple(p) for p in item['state'][1])): item['value']
                        for item in answers['heuristics']
                    }
                check_definition(api, problem, check_heuristic=question == 'Q6',
                                 expected_heuristics=expected_heuristics)
                if question == 'Q6':
                    print(f'{name} heuristic: PASSED')
                else:
                    print(f'{name} problem definition: PASSED')
            problem['start_state'] = api.initial_state(problem)
            if describe(api, problem['start_state']) != (problem['pacman_start'], problem['food_positions']):
                raise ValueError('Incorrect initial state.')
            phase = algorithm
            candidate = search(problem)
            observed = validate_result(api, problem, candidate)
            problem.pop('start_state')
            if repr(problem) != original:
                raise ValueError('Do not modify problem or its grid.')
            result = candidate
            print(f'Checking {question}: {name}' if options.test else f'Running {question}: {name}')
            search_summary(result)
            if options.test:
                expected = json.loads(available[name].with_name(name + '_expected.json').read_text(encoding='utf-8'))['result']
                # JSON arrays describe observable position/food, independent of student state types.
                def display(state):
                    position, food = state
                    return f'position={tuple(position)}, remaining food={tuple(tuple(p) for p in food)}'
                compare_result(json.loads(json.dumps(observed)), expected, display)
                print(f'{name}: PASSED')
            passed += 1
        except Exception as error:
            print(f'{name} {phase}: FAILED\n{error_detail(error)}')
            if unfinished_dependency(error, {'q1.py', 'q2.py', 'q5.py'}) and not options.visualize:
                remaining = len(names) - names.index(name) - 1
                if remaining:
                    print(f'Remaining {remaining} cases: SKIPPED until the unfinished function is implemented.')
                stop = True
        if options.visualize:
            if result is not None:
                replay(api, problem, result)
            else:
                print(f'Maze preview only: complete or fix the {question} functions.')
                display = dict(preview_problem, start_state=preview_problem['pacman_start'], goal_states=preview_problem['food_positions'])
                print('\n'.join(maze_lines(display)))
        if stop:
            break
    return finish(question, passed, len(names)) if options.test else (0 if passed == len(names) else 1)
