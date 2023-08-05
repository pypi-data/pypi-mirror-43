
import itertools
import sys

import contextlib
import gzip
import lzma
from multiprocessing.pool import Pool


def slicing_window(seq, n):
    """Iterate over a sequence in windows of size n"""
    it = iter(seq)
    result = ''.join(itertools.islice(it, n))

    if len(result) == n:
        yield result

    for elem in it:
        result = result[1:] + elem
        yield result


def chunkizator(iterable, size=1000):
    """Creates chunks from an iterable"""
    s = 0
    chunk = []
    for i in iterable:
        if s == size:
            yield chunk
            chunk = []
            s = 0
        chunk.append(i)
        s += 1
    yield chunk


def sum_parallel(function, items, initial, chuck_size, cores):
    """Call a function in parallel and sum the output to the initial value"""
    value = initial
    with Pool(int(cores)) as pool:
        for c in pool.imap_unordered(function, chunkizator(items, size=chuck_size)):
            value += c
    return value


def __open_file(file, mode="rt"):
    """Open file with different compression formats"""

    # Detect open method
    if file.endswith('gz') or file.endswith('bgz'):
        open_method = gzip.open
    elif file.endswith('xz'):
        open_method = lzma.open
    else:
        open_method = open

    return open_method(file, mode)


@contextlib.contextmanager
def file_open(file=None, mode='wt'):
    """
    Open file in write mode or send to STDOUT
    if file is None
    """
    if file:
        fh = __open_file(file, mode)
    else:
        fh = sys.stdout
    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()
