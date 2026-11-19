"""Console displays are explanatory; their spacing is not graded."""

def show_map(problem):
    print('Map:', problem['map_file'], '| coordinates: (row, column)')
    print('  ' + ''.join(str(c % 10) for c in range(len(problem['grid'][0]))))
    for r, row in enumerate(problem['grid']):
        print(str(r) + ' ' + row)
    if problem['kind'] == 'mdp':
        print('● start; █ wall; + / - exit cells (reward paid on Exit)')
        print('noise:', problem['noise'], 'living reward:', problem['living_reward'],
              'discount:', problem['discount'])
    else:
        print('● fixed observer; █ wall; ghost may occupy any non-wall cell')


def show_values(problem, values, title):
    print('\n' + title)
    width = 9
    print('    ' + ''.join(f'{c:>{width}}' for c in range(len(problem['grid'][0]))))
    for r, row in enumerate(problem['grid']):
        cells = []
        for c in range(len(row)):
            value = values.get((r, c))
            cells.append('█' if value is None else
                         f'{value:.4f}' if isinstance(value, (int, float)) else str(value))
        print(f'{r:>3} ' + ''.join(f'{v:>{width}}' for v in cells))
