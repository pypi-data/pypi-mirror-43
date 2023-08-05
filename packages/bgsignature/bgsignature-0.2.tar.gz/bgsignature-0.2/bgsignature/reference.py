"""Utilities related to the reference genome"""

from bgreference import refseq


def get_seq(genome, chromosome, start, size=1):
    """Get a sequence from the reference genome"""
    return refseq(genome, chromosome, start, size)


def get_kmer(genome, chromosome, pos, size=3):
    """Get the kmer around a position"""
    start = pos - size//2
    return get_seq(genome, chromosome, start, size)


def get_reg(genome, chromosome, start, stop, size=3):
    """Get a region extending """
    total = (stop - start + 1) + (size - 1)
    start_ = start - size//2
    return get_seq(genome, chromosome, start_, total)


__CB = {"A": "T", "T": "A", "G": "C", "C": "G"}


def reverse_complementary(seq):
    return "".join([__CB.get(base, base) for base in seq[::-1]])
