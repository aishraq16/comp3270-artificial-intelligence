"""Shared maze symbols, supplied for use in the question files and helpers."""

WALL = '█'
PACMAN = '●'
FOOD = '·'
EMPTY = ' '

# Same action names and North, East, South, West ordering as A1.
DIRECTIONS = (('North', (-1, 0)), ('East', (0, 1)),
              ('South', (1, 0)), ('West', (0, -1)))
