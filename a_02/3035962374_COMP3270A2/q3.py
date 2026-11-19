"""COMP3270 A2 Q3: complete only the marked functions."""

def turn_order(problem):
    """Return tuple ('P', ...present ghost labels in alphabetical order...).
    Example with W and Y: ('P', 'W', 'Y'). Do not invent missing ghosts.
    problem['ghosts'] maps labels to start coordinates; do not modify it."""
    return ('P',) + tuple(sorted(problem['ghosts']))

def next_turn(problem, agent, depth):
    """Return (next_agent, next_depth). agent is present in turn_order(problem).
    depth is a positive integer counting complete rounds, not individual moves.
    Keep depth on every turn except the last ghost: return ('P', depth-1) then.
    A stuck ghost still takes a passing turn. Do not modify problem."""
    order = turn_order(problem)
    index = order.index(agent)
    if index == len(order) - 1:
        return ('P', depth - 1)
    return (order[index + 1], depth)

# Supplied runner: leave everything below unchanged.
if __name__ == '__main__':
    from support.runner import entry
    raise SystemExit(entry(3))
