"""Fake the refseq method of the bgrefence package
to ensure a known and well defined genome when needed"""


import itertools
import bgreference

original_refseq = bgreference.refseq  # keep original function


def repeat_acgt(genome, chromosome, start, size=1):
    """Build a genome by repeating ACGT sequences"""
    pos = start % 4
    seq = 'TACGTACG'[pos:pos+4]
    return ''.join([v for _, v in zip(range(size), itertools.cycle(seq))])


def repeat_acgtn(genome, chromosome, start, size=1):
    """Build a genome by repeating ACGTN sequences"""
    pos = start % 5
    seq = 'NACGTNACGT'[pos:pos+5]
    return ''.join([v for _, v in zip(range(size), itertools.cycle(seq))])


def refseq(genome, chromosome, start, size=1):
    """Fake bgreference.refseq function that included
    other genomes not using bgdata"""
    if genome == 'acgt':
        return repeat_acgt('', chromosome, start, size)
    elif genome == 'acgtn':
        return repeat_acgtn('', chromosome, start, size)
    else:
        return original_refseq(genome, chromosome, start, size)


bgreference.refseq = refseq  # replace the function with our
