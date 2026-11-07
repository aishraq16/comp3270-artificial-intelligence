"""Supplied console runner and public checks; no assessed algorithm solutions."""
import argparse
import copy
import importlib
import json
import math
import random
import sys
from pathlib import Path

from support.constants import DIRECTIONS
from support.game import (ROOT, choose_reflex, initial_state, load_case, render,
                          state_from_json, state_to_json)



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
    if frame is None and isinstance(error, SyntaxError):
        name = Path(error.filename or '').name
        if name in {f'q{n}.py' for n in range(7)}:
            frame = (name, error.lineno, 'module')
    location = f'{frame[0]}:{frame[1]} in {frame[2]}\n' if frame else ''
    message = f'{location}{type(error).__name__}: {error}'
    if isinstance(error, NotImplementedError) and frame:
        message += (f'\nComplete {frame[2]} in {frame[0]} first. '
                    f'Then run python3 {frame[0]} --test.')
    return message


def modules(question, helper_only=False):
    needed = {0: (0,), 1: (1,), 2: (1, 2), 3: (1, 3),
              4: (1, 3, 4), 5: (1, 3, 5), 6: (1, 3, 6)}[question]
    if helper_only and question == 3:
        needed = (3,)
    elif helper_only and question == 4:
        needed = (1, 4)
    return {q: importlib.import_module(f'q{q}') for q in needed}


def validate_actions(actions):
    labels = [label for label, _ in DIRECTIONS]
    if type(actions) is not list or any(type(a) is not str or a not in labels for a in actions):
        raise ValueError('legal_actions must return a list of direction strings.')
    if actions != [a for a in labels if a in actions]:
        raise ValueError('Legal actions must be unique and in North/East/South/West order.')
    return actions


def validate_state(child, problem, parent):
    if type(child) is not dict or set(child) != {'pos', 'ghosts', 'food', 'score', 'winner'}:
        raise ValueError('A successor must be a dictionary with exactly the documented state fields.')
    if child is parent or child['ghosts'] is parent['ghosts']:
        raise ValueError('successor must create independent state and ghosts dictionaries.')
    if type(child['ghosts']) is not dict or set(child['ghosts']) != set(problem['ghosts']):
        raise ValueError('State ghosts must be a dictionary containing the present ghost labels.')
    if type(child['food']) is not frozenset or type(child['score']) is not int:
        raise ValueError('State food must be a frozenset and score an integer.')
    positions = [child['pos'], *child['ghosts'].values(), *child['food']]
    if any(type(p) is not tuple or len(p) != 2 or any(type(v) is not int for v in p)
           for p in positions):
        raise ValueError('Positions and food coordinates must be pairs of integers in tuples.')
    if child['winner'] not in (None, 'Pacman', 'Ghost'):
        raise ValueError("winner must be None, 'Pacman' or 'Ghost'.")


def validate_search(result):
    if type(result) is not dict or set(result) != {'action', 'value', 'expanded'}:
        raise ValueError('Search must return exactly action, value and expanded.')
    labels = [label for label, _ in DIRECTIONS]
    if result['action'] is not None and result['action'] not in labels:
        raise ValueError('Search action must be a direction string or None.')
    if type(result['expanded']) is not int or result['expanded'] < 0:
        raise ValueError('expanded must be a nonnegative integer.')
    if type(result['value']) not in (int, float) or not math.isfinite(result['value']):
        raise ValueError('value must be a finite number.')


class CountingRandom(random.Random):
    """The normal seeded RNG with an observable count of choice calls."""
    def __init__(self, seed):
        super().__init__(seed)
        self.choice_calls = 0

    def choice(self, sequence):
        self.choice_calls += 1
        return super().choice(sequence)


def run_game(question, problem, funcs, seed=8, depth=2, max_rounds=100):
    """Returns structured frames; a timeout is unfinished, never a win."""
    state = initial_state(problem)
    rng = random.Random(seed)
    order = funcs[3].turn_order(problem) if question >= 3 else ('P', *problem['ghosts'])
    frames = [(None, None, copy.deepcopy(state))]
    expanded = 0
    for _ in range(max_rounds):
        for agent in order:
            if state['winner'] is not None:
                return frames, expanded
            before = copy.deepcopy((problem, state))
            if question == 5:
                result = funcs[5].minimax(problem, state, agent, depth)
                validate_search(result)
                action = result['action']
                expanded += result['expanded']
            elif question == 6 and agent == 'P':
                result = funcs[6].expectimax(problem, state, 'P', depth)
                validate_search(result)
                action = result['action']
                expanded += result['expanded']
            elif agent == 'P' and question in (2, 4):
                action = choose_reflex(problem, state, funcs[question].evaluate_action,
                                       funcs[1].successor, funcs[1].legal_actions)
            else:
                action = funcs[1].random_action(problem, state, agent, rng)
            legal = validate_actions(funcs[1].legal_actions(problem, state, agent))
            if (legal and action not in legal) or (not legal and action is not None):
                raise ValueError(f'{agent} returned illegal action {action!r}.')
            child = funcs[1].successor(problem, state, agent, action)
            validate_state(child, problem, state)
            if (problem, state) != before:
                raise ValueError('A function modified its problem or parent state.')
            state = child
            frames.append((agent, action, copy.deepcopy(state)))
    return frames, expanded


def same(actual, expected):
    if isinstance(expected, dict):
        return isinstance(actual, dict) and actual.keys() == expected.keys() and all(
            same(actual[k], expected[k]) for k in expected)
    if isinstance(expected, list):
        return isinstance(actual, (tuple, list)) and len(actual) == len(expected) and all(
            same(a, b) for a, b in zip(actual, expected))
    if isinstance(expected, (int, float)) and not isinstance(expected, bool):
        return isinstance(actual, (int, float)) and not isinstance(actual, bool) and math.isclose(
            actual, expected, rel_tol=1e-9, abs_tol=1e-9)
    return actual == expected


def action_values(question, problem, state, funcs, evaluator=None):
    actions = validate_actions(funcs[1].legal_actions(problem, state, 'P')) or [None]
    before = copy.deepcopy((problem, state))
    values = []
    evaluator = funcs[question].evaluate_action if evaluator is None else evaluator
    for action in actions:
        value = evaluator(problem, state, action)
        if type(value) not in (int, float) or not math.isfinite(value):
            raise ValueError('Every action must receive a finite numerical evaluation.')
        child = funcs[1].successor(problem, state, 'P', action)
        validate_state(child, problem, state)
        if child['winner'] is not None and value != child['score']:
            raise ValueError('Terminal successors must receive their final game score.')
        if (problem, state) != before:
            raise ValueError('A function modified its problem or parent state.')
        values.append(value)
    selected = actions[max(range(len(actions)), key=lambda i: values[i])]
    return actions, values, selected


def check_result(question, case, problem, funcs):
    """Public fixture results. Inputs and expected answers are separate files."""
    state = state_from_json(case['state']) if 'state' in case else initial_state(problem)
    before = copy.deepcopy((problem, state))
    q = funcs[question]
    if question == 0:
        result = q.manhattan(tuple(case['a']), tuple(case['b']))
        if type(result) is not int or result < 0:
            raise ValueError('manhattan must return a nonnegative integer.')
    elif question == 1:
        agent = case.get('agent', 'P')
        operation = case['operation']
        if operation == 'actions':
            result = validate_actions(q.legal_actions(problem, state, agent))
        elif operation == 'successor':
            child = q.successor(problem, state, agent, case['action'])
            validate_state(child, problem, state)
            result = state_to_json(child)
        elif operation == 'invalid_successor':
            try:
                q.successor(problem, state, agent, case['action'])
            except ValueError:
                result = {'raises': 'ValueError'}
            else:
                raise AssertionError('An invalid move or unnecessary pass must raise ValueError.')
        elif operation == 'random':
            rng = CountingRandom(case['seed'])
            control = random.Random(case['seed'])
            result = []
            for _ in range(5):
                actions = validate_actions(q.legal_actions(problem, state, agent))
                calls, rng_before = rng.choice_calls, rng.getstate()
                action = q.random_action(problem, state, agent, rng)
                required_calls = int(bool(actions))
                if rng.choice_calls - calls != required_calls:
                    raise ValueError('random_action must call rng.choice once for a move and zero times for a pass.')
                if not actions and rng.getstate() != rng_before:
                    raise ValueError('A forced pass must not change the RNG state.')
                expected_action = control.choice(actions) if actions else None
                if action != expected_action or rng.getstate() != control.getstate():
                    raise ValueError('Use exactly the supplied rng.choice on the legal action list; do not reseed or consume extra randomness.')
                result.append(action)
        elif operation == 'game':
            frames, expanded = run_game(1, problem, funcs, case['seed'], max_rounds=case['max_rounds'])
            result = {'moves': [[g, a] for g, a, _ in frames[1:]],
                      'final': state_to_json(frames[-1][2]), 'expanded': expanded}
        else:
            raise ValueError(f'Unknown Q1 operation: {operation}.')
    elif question in (2, 4):
        actions, _, action = action_values(question, problem, state, funcs)
        result = {'legal': action in actions, 'finite': True}
        if 'must_choose' in case:
            result['action'] = action
    elif question == 3:
        order = q.turn_order(problem)
        nxt = q.next_turn(problem, case['agent'], case['depth'])
        if type(order) is not tuple or any(type(a) is not str for a in order):
            raise ValueError('turn_order must return a tuple of agent labels.')
        if type(nxt) is not tuple or len(nxt) != 2 or type(nxt[0]) is not str or type(nxt[1]) is not int:
            raise ValueError('next_turn must return a (next_agent, next_depth) tuple.')
        result = {'order': list(order), 'next': list(nxt)}
    else:
        search = q.minimax if question == 5 else q.expectimax
        result = search(problem, state, case.get('agent', 'P'), case['depth'])
        validate_search(result)
    if (problem, state) != before:
        raise ValueError('A function modified its problem or parent state.')
    return result


def case_paths(question):
    folder = ROOT / 'test_cases' / f'q{question}'
    return sorted(p for p in folder.glob('*.json') if not p.name.endswith('_expected.json'))


def run_tests(question, funcs, name=None, stage=None):
    paths = []
    for path in case_paths(question):
        case = json.loads(path.read_text(encoding='utf-8'))
        if name is not None and path.stem != Path(name.replace('\\', '/')).stem:
            continue
        if case.get('written_only', False):
            if name is not None:
                raise ValueError(f'{path.stem} is a written input without a public answer key. Use python3 q{question}.py {path.stem} --inspect.')
            continue
        operation = case.get('operation')
        if stage is not None:
            allowed = {'actions': {'actions'}, 'successor': {'successor', 'invalid_successor'}, 'random': {'random'}}[stage]
            if operation not in allowed:
                continue
        paths.append(path)
    if question == 1:
        phases = {'actions': 0, 'successor': 1, 'invalid_successor': 2, 'random': 3, 'game': 4}
        paths.sort(key=lambda p: (phases[json.loads(p.read_text())['operation']], p.stem))
    if not paths:
        raise ValueError('No matching public checks. Use --list to choose a case and compatible stage.')
    passed = 0
    for path in paths:
        try:
            case, problem = load_case(question, path.name)
            expected = json.loads(path.with_name(path.stem + '_expected.json').read_text(encoding='utf-8'))
            actual = check_result(question, case, problem, funcs)
            if question == 4:
                # The comparison has the same type, purity and terminal-score
                # contract, but removing a feature may change its chosen move.
                state = state_from_json(case['state']) if 'state' in case else initial_state(problem)
                action_values(question, problem, state, funcs,
                              funcs[4].evaluate_action_without_feature)
            if same(actual, expected):
                print(f'{path.stem}: PASSED' + (f" | Expanded: {actual['expanded']}" if question in (5, 6) else ''))
                passed += 1
            else:
                print(f'{path.stem}: FAILED\nExpected: {expected!r}\nActual:   {actual!r}')
        except Exception as exc:
            print(f'{path.stem}: FAILED\n{error_detail(exc)}')
    print(f'Q{question}: {passed}/{len(paths)} public checks passed')
    if question in (2, 4):
        print('These checks cover contracts and immediate outcomes. Evaluation quality is marked separately.')
    return 0 if passed == len(paths) else 1


def replay(problem, frames, expanded=None, max_frames=None):
    """Line-input playback works in Windows PowerShell and macOS Terminal."""
    for index, (agent, action, state) in enumerate(frames):
        if max_frames is not None and index >= max_frames:
            break
        print(f'Frame {index}: initial state' if agent is None else
              f'Frame {index}: {agent} moves {action or "PASS"}')
        print(render(problem, state))
        if expanded is not None:
            print(f'Expanded nodes across completed game: {expanded}')
        if state['winner']:
            print('Winner:', state['winner'])
        if not sys.stdin.isatty():
            continue
        try:
            if input('Enter: next frame | q: quit > ').strip().lower() == 'q':
                break
        except (EOFError, KeyboardInterrupt):
            print('\nReplay ended.')
            break


def game_case(question, case, problem):
    return (question != 0 and 'state' not in case and case.get('agent', 'P') == 'P'
            and (question not in (1, 2) or len(problem['ghosts']) == 1)
            and case.get('depth', 2) > 0)


def inspect_result(question, case, problem, funcs, branches=False, ablate=False):
    state = state_from_json(case['state']) if 'state' in case else initial_state(problem)
    result = check_result(question, case, problem, funcs)
    if question == 0:
        print('Distance:', result)
    elif question == 1:
        print('Operation:', case['operation'], '| Agent:', case.get('agent', 'P'))
        if case['operation'] == 'game':
            result = {key: value for key, value in result.items() if key != 'expanded'}
        print('Result:', result)
    elif question in (2, 4):
        actions, values, selected = action_values(question, problem, state, funcs)
        print('Action | Value')
        for action, value in zip(actions, values):
            print(f'{action or "PASS"} | {value}')
        print('Selected action:', selected or 'PASS')
        if ablate:
            actions, values, selected = action_values(
                question, problem, state, funcs, funcs[4].evaluate_action_without_feature)
            print('Without additional feature:')
            print('Action | Value')
            for action, value in zip(actions, values):
                print(f'{action or "PASS"} | {value}')
            print('Selected action without feature:', selected or 'PASS')
    elif question == 3:
        print('Turn order:', tuple(result['order']))
        print('Current agent:', case['agent'], '| Depth:', case['depth'])
        print('Next turn:', tuple(result['next']))
    else:
        agent, depth = case.get('agent', 'P'), case['depth']
        print('Root agent:', agent, '| Depth:', depth)
        print('Action:', result['action'])
        print('Value:', result['value'])
        print('Expanded nodes:', result['expanded'])
        if branches:
            if state['winner'] is not None or depth == 0:
                print('Root is a leaf: no branches.')
                return
            print('Root branches (additional inspection calls; excluded from the root count above):')
            actions = validate_actions(funcs[1].legal_actions(problem, state, agent)) or [None]
            chance = question == 6 and agent != 'P'
            backup = 'uniform mean' if chance else ('maximum' if agent == 'P' else 'minimum')
            print('Root backup:', backup)
            print('Action | Child value | Child expanded nodes' + (' | Probability' if chance else ''))
            next_agent, next_depth = funcs[3].next_turn(problem, agent, depth)
            search = funcs[question].minimax if question == 5 else funcs[question].expectimax
            before = copy.deepcopy((problem, state))
            for action in actions:
                child = funcs[1].successor(problem, state, agent, action)
                validate_state(child, problem, state)
                child_before = copy.deepcopy(child)
                backed_up = search(problem, child, next_agent, next_depth)
                validate_search(backed_up)
                if child != child_before or (problem, state) != before:
                    raise ValueError('Branch inspection found a modified input state or problem.')
                line = f"{action or 'PASS'} | {backed_up['value']} | {backed_up['expanded']}"
                print(line + (f' | 1/{len(actions)}' if chance else ''))


def main(question, argv=None):
    parser = argparse.ArgumentParser(description=f'COMP3270 A2 Q{question}; run from student/.', allow_abbrev=False)
    parser.add_argument('case', nargs='?', default=None, help='case name, name.json or test_cases/qN/name.json')
    parser.add_argument('-t', '--test', action='store_true', help='check all public cases, or one named case')
    parser.add_argument('-l', '--list', action='store_true', help='list case paths and suitable modes')
    parser.add_argument('-m', '--show-maze', action='store_true', help='show the actual fixture board without calling your code')
    parser.add_argument('--inspect', action='store_true', help='inspect the fixture operation instead of playing a game')
    if question == 4:
        parser.add_argument('--ablate', action='store_true', help='with --inspect, compare your evaluation with your additional feature removed')
    if question == 1:
        parser.add_argument('--stage', choices=('actions', 'successor', 'random'), help='limit --test to one implementation stage')
    if question != 0:
        parser.add_argument('-r', '--replay', action='store_true', help='step through a completed game')
        parser.add_argument('--trials', type=int, default=1)
        parser.add_argument('--seed', type=int, default=None, help='base seed; trial i uses seed+i (i starts at zero)')
        parser.add_argument('--max-rounds', type=int, default=None)
    if question in (5, 6):
        parser.add_argument('--depth', type=int, default=None, help='remaining round completions, not individual turns')
        parser.add_argument('--branches', action='store_true', help='with --inspect, show root child values from additional calls to your search')
    args = parser.parse_args(argv)
    visualize = args.show_maze or args.inspect or getattr(args, 'replay', False)
    if args.list and (args.test or visualize):
        parser.error('--list cannot be combined with --test, --show-maze, --inspect or --replay.')
    if args.test and visualize and args.case is None:
        parser.error('Select one named case when combining --test with --show-maze, --inspect or --replay.')
    if args.inspect and getattr(args, 'replay', False):
        parser.error('--inspect and --replay describe different modes; choose one.')
    if getattr(args, 'ablate', False) and not args.inspect:
        parser.error('Use --ablate with --inspect, for example: python3 q4.py crossroads --inspect --ablate.')
    if getattr(args, 'branches', False) and not args.inspect:
        parser.error('Use --branches with --inspect, for example: python3 q5.py corridor --inspect --branches.')
    if getattr(args, 'stage', None) is not None and not args.test:
        parser.error('--stage requires --test, for example: python3 q1.py --test --stage actions.')
    if args.list:
        for path in case_paths(question):
            case, problem = load_case(question, path.name)
            modes = ['preview', 'inspect']
            if not case.get('written_only', False):
                modes.append('test')
            if game_case(question, case, problem):
                modes.extend(('game', 'replay'))
            print(path.relative_to(ROOT).as_posix() + ' [' + ', '.join(modes) + ']')
        return 0
    if args.test and not visualize:
        if args.case is not None:
            load_case(question, args.case)
        return run_tests(question, modules(question, helper_only=True), args.case, getattr(args, 'stage', None))
    name = args.case or 'corridor'
    case, problem = load_case(question, name)
    inspected = dict(case)
    if getattr(args, 'depth', None) is not None:
        if args.depth < 0:
            raise ValueError('Inspection depth must be nonnegative.')
        inspected['depth'] = args.depth
    state = state_from_json(case['state']) if 'state' in case else initial_state(problem)
    print(f'Running Q{question}: {Path(name).stem}')
    print(render(problem, state))
    test_code = 0
    if args.test:
        test_code = run_tests(question, modules(question, helper_only=True), name, getattr(args, 'stage', None))
    if args.show_maze and not args.inspect and not getattr(args, 'replay', False):
        return test_code
    funcs = modules(question, helper_only=args.inspect)
    if args.inspect:
        inspect_result(question, inspected, problem, funcs, getattr(args, 'branches', False), getattr(args, 'ablate', False))
        return test_code
    if question == 0:
        print('Distance:', check_result(question, case, problem, funcs))
        return test_code
    if not game_case(question, inspected, problem):
        raise ValueError(f'This fixture is for inspection, not initial-state gameplay. Use python3 q{question}.py {Path(name).stem} --inspect or --show-maze.')
    if args.trials <= 0:
        raise ValueError('--trials must be positive.')
    depth = inspected.get('depth', 2)
    seed = case.get('seed', 8) if args.seed is None else args.seed
    limit = case.get('max_rounds', 100) if args.max_rounds is None else args.max_rounds
    if depth <= 0 or limit <= 0:
        raise ValueError('Game depth and --max-rounds must be positive.')
    print(f'Base seed: {seed} | Trials: {args.trials} | Max rounds: {limit}')
    if question in (5, 6):
        print(f'Depth: {depth} remaining round completions')
    winners = {'Pacman': 0, 'Ghost': 0, 'Unfinished': 0}
    for trial in range(args.trials):
        frames, expanded = run_game(question, problem, funcs, seed+trial, depth, limit)
        final = frames[-1][2]
        outcome = final['winner'] or 'Unfinished'
        winners[outcome] += 1
        pacman_turns = sum(agent == 'P' for agent, _, _ in frames[1:])
        summary = f"Trial {trial+1}: {outcome}, score {final['score']}, Pacman turns {pacman_turns}"
        if question in (5, 6):
            summary += f", expanded {expanded}"
        print(summary)
        if args.replay:
            replay(problem, frames, expanded if question in (5, 6) else None)
    print(f"Wins: {winners['Pacman']}/{args.trials} | Losses: {winners['Ghost']} | Unfinished: {winners['Unfinished']}")
    return test_code


def entry(question):
    try:
        return main(question)
    except KeyboardInterrupt:
        print('Run interrupted.', file=sys.stderr)
        return 130
    except Exception as exc:
        print(error_detail(exc), file=sys.stderr)
        return 1
