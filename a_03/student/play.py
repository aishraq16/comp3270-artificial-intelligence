"""Supplied experiments. Run python3 play.py --help for available commands."""
import argparse
import importlib
from support.models import load_problem, actions
from support.display import show_map, show_values
from support.experiments import train, filter_trace, particle_trace, total_variation


def main():
    parser = argparse.ArgumentParser(description='COMP3270 A3 experiments')
    parser.add_argument('mode', choices=('vi', 'learn', 'exact', 'particles', 'compare'))
    parser.add_argument('--map', default=None)
    parser.add_argument('--iterations', type=int, default=100)
    parser.add_argument('--episodes', type=int, default=1000)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--count', type=int, default=130)
    parser.add_argument('--readings', default='2,3,2')
    args = parser.parse_args()
    if args.iterations < 0 or args.episodes < 1 or args.count < 1:
        parser.error('iterations must be nonnegative; episodes/count positive')
    try:
        readings = [int(x) for x in args.readings.split(',')]
        if any(x < 0 for x in readings):
            raise ValueError()
    except ValueError:
        parser.error('readings must be comma-separated nonnegative integers')
    mdp_mode = args.mode in ('vi', 'learn')
    problem = load_problem(args.map or ('gridworld' if mdp_mode else 'ghost_room'))
    if (problem['kind'] == 'mdp') != mdp_mode:
        parser.error('Use an MDP map for vi/learn; an HMM map for other modes')
    show_map(problem)
    if args.mode == 'vi':
        q1 = importlib.import_module('q1')
        values = q1.value_iteration(problem, args.iterations)
        show_values(problem, values, f'V after {args.iterations} sweeps')
        policy = {s: max(actions(problem, s),
                        key=lambda a: q1.action_value(problem, s, a, values))
                  for s in problem['states']}
        show_values(problem, policy, 'Greedy policy from these values (one-step lookahead)')
        print('Start value:', values[problem['start']], '| action:', policy[problem['start']])
    elif args.mode == 'learn':
        q2 = importlib.import_module('q2')
        values, completed = train(problem, q2.choose_action, q2.q_update,
                                  args.episodes, args.seed)
        policy = {s: max(actions(problem, s), key=lambda a: values.get((s, a), 0))
                  for s in problem['states']}
        show_values(problem, {s: values.get((s, policy[s]), 0) for s in problem['states']},
                    'Largest learned Q at each state')
        show_values(problem, policy, 'Learned greedy policy (first maximum)')
        print('Episodes:', args.episodes, '| seed:', args.seed,
              '| ended with Exit:', completed, '| cut off:', args.episodes - completed)
        print('Start Q:', values.get((problem['start'], policy[problem['start']]), 0),
              '| action:', policy[problem['start']])
    else:
        exact = sampled = None
        if args.mode in ('exact', 'compare'):
            q3 = importlib.import_module('q3')
            exact = filter_trace(problem, q3.predict, q3.observe, readings)
        if args.mode in ('particles', 'compare'):
            q4 = importlib.import_module('q4')
            sampled = particle_trace(problem, q4.predict_particles, q4.observe_particles,
                                     readings, args.count, args.seed)
        for t, reading in enumerate(readings, 1):
            print(f'\nTime {t}; new evidence: distance reading {reading}')
            for label, history in [('Exact', exact), ('Particles', sampled)]:
                if history is not None:
                    show_values(problem, history[t-1][0], label + ': Time Passes, B prime')
                    show_values(problem, history[t-1][1], label + ': New Evidence, B')
            if exact is not None and sampled is not None:
                print('Total variation:', total_variation(exact[t-1][1], sampled[t-1][1]))
        if sampled is not None:
            print('Particle count:', args.count, '| seed:', args.seed)


if __name__ == '__main__':
    try:
        main()
    except (NotImplementedError, ValueError) as error:
        raise SystemExit(str(error))
