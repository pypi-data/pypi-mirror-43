"""Utilities for loading and saving signatures"""

import json

from bgsignature.utils import file_open


def load(file):
    """Load from a JSON file"""
    with file_open(file, 'rt') as fd:
        return json.load(fd)


def save(dict_, file=None):
    """Save to a JSON file"""
    if file is None or file.endswith('.json'):
        indent = 4
    else:
        indent = None

    with file_open(file, 'wt') as fd:
        json.dump(dict_, fd, indent=indent)
