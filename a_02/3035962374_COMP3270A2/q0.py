"""COMP3270 A2 Q0: complete only the marked functions."""

def manhattan(a, b):
    """Return the Manhattan distance between coordinate tuples a and b.
    Rows and columns may be negative. Do not modify inputs."""
    # Your Q0 code here
    #raise NotImplementedError('Implement manhattan')
    x_a, y_a = a
    x_b, y_b = b
    return abs(x_a - x_b) + abs(y_a - y_b)

# Supplied runner: leave everything below unchanged.
if __name__ == '__main__':
    from support.runner import entry
    raise SystemExit(entry(0))
