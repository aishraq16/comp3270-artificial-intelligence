"""Outside coordinate labels, identical to Assignment 1."""

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

