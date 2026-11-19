"""Keep maze symbols readable when Windows redirects output to a file or pipe."""
import sys


def prepare_maze_output():
    stream = sys.stdout
    encoding = getattr(stream, 'encoding', None)
    if not encoding or not callable(getattr(stream, 'reconfigure', None)):
        return
    try:
        '█●·░○◎─│'.encode(encoding)
    except UnicodeEncodeError:
        # Real Unicode terminals remain unchanged; legacy redirected streams
        # need UTF-8 to retain the same maze symbols without an encoding error.
        stream.reconfigure(encoding='utf-8')
