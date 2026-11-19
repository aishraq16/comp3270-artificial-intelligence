"""Normalize supplied input names consistently for all assignment commands."""
import argparse


def input_name(value, folder):
    """Accept a stem, JSON filename or path relative to the student folder."""
    name = value.replace('\\', '/').removeprefix('./')
    if name.startswith(folder + '/'):
        name = name[len(folder) + 1:]
    if '/' in name or name in ('.', '..'):
        raise argparse.ArgumentTypeError(f'Choose an input from {folder}/; use --list to see files.')
    return name.removesuffix('.json')
