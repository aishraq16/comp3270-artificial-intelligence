"""Supplied path ordering, independent of Q5's chosen state containers."""
def path_key(path, position, food):
    return tuple((position(state), food(state)) for state in path)
