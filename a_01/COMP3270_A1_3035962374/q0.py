"""Q0: implement a short, zero-mark warm-up to learn the workflow."""


def count_moves(path):
    # Your Q0 code here: return the number of moves in this nonempty path.
    # The path lists the starting state and the states reached after each move.
    return len(path) - 1


# Supplied runner: leave everything below unchanged.
# Run: python3 q0.py   |   Test: python3 q0.py --test
if __name__ == '__main__':
    import sys
    from support.grader import grade_q0

    raise SystemExit(grade_q0(count_moves, sys.argv[1:]))
