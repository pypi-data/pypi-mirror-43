from . import reference

from os import path

import bgsignature


def test_simple(tmpdir):
    """Simple test of a mutations file"""
    lines = ['\t'.join(['CHR', 'POS', 'REF', 'ALT'])]
    lines.append('\t'.join(['1', '5', 'A', 'C']))
    lines.append('\t'.join(['1', '6', 'C', 'T']))

    mut_file = path.join(str(tmpdir), 'mut.tsv')
    with open(mut_file, 'w') as fd:
        fd.write('\n'.join(lines))

    counts = bgsignature.count(mut_file, None, kmer_size=3, genome_build='acgt',
                               collapse=False, includeN=False, group=None, cores=None)

    assert len(counts) == 2
    assert counts['TAC>C'] == 1
    assert counts['ACG>T'] == 1


def test_wrong_ref(tmpdir):
    """Mutation with incorrect reference"""
    lines = ['\t'.join(['CHR', 'POS', 'REF', 'ALT'])]
    lines.append('\t'.join(['1', '5', 'A', 'C']))
    lines.append('\t'.join(['1', '6', 'C', 'T']))
    lines.append('\t'.join(['1', '7', 'C', 'T']))

    mut_file = path.join(str(tmpdir), 'mut.tsv')
    with open(mut_file, 'w') as fd:
        fd.write('\n'.join(lines))

    counts = bgsignature.count(mut_file, None, kmer_size=3, genome_build='acgt',
                               collapse=False, includeN=False, group=None, cores=None)

    assert len(counts) == 2
    assert counts['TAC>C'] == 1
    assert counts['ACG>T'] == 1


def test_collapse(tmpdir):
    """Collapse mutations"""
    lines = ['\t'.join(['CHR', 'POS', 'REF', 'ALT'])]
    lines.append('\t'.join(['1', '5', 'A', 'C']))
    lines.append('\t'.join(['1', '6', 'C', 'T']))

    mut_file = path.join(str(tmpdir), 'mut.tsv')
    with open(mut_file, 'w') as fd:
        fd.write('\n'.join(lines))

    counts = bgsignature.count(mut_file, None, kmer_size=3, genome_build='acgt',
                               collapse=True, includeN=False, group=None, cores=None)

    assert len(counts) == 4
    assert counts['TAC>C'] == 1
    assert counts['GTA>G'] == 1
    assert counts['ACG>T'] == 1
    assert counts['CGT>A'] == 1


def test_group(tmpdir):
    """Group mutations by sample"""
    lines = ['\t'.join(['CHR', 'POS', 'REF', 'ALT', 'SAMPLE'])]
    lines.append('\t'.join(['1', '5', 'A', 'C', 'X']))
    lines.append('\t'.join(['1', '6', 'C', 'T', 'X']))
    lines.append('\t'.join(['1', '6', 'C', 'T', 'Y']))

    mut_file = path.join(str(tmpdir), 'mut.tsv')
    with open(mut_file, 'w') as fd:
        fd.write('\n'.join(lines))

    counts = bgsignature.count(mut_file, None, kmer_size=3, genome_build='acgt',
                               collapse=False, includeN=False, group='SAMPLE', cores=None)

    assert len(counts) == 2
    counts_x = counts['X']
    assert len(counts_x) == 2
    assert counts_x['TAC>C'] == 1
    assert counts_x['ACG>T'] == 1
    counts_y = counts['Y']
    assert len(counts_y) == 1
    assert counts_y['ACG>T'] == 1


def test_group_collapse(tmpdir):
    """Group mutations by sample and collapse"""
    lines = ['\t'.join(['CHR', 'POS', 'REF', 'ALT', 'SAMPLE'])]
    lines.append('\t'.join(['1', '5', 'A', 'C', 'X']))
    lines.append('\t'.join(['1', '6', 'C', 'T', 'X']))
    lines.append('\t'.join(['1', '6', 'C', 'T', 'Y']))

    mut_file = path.join(str(tmpdir), 'mut.tsv')
    with open(mut_file, 'w') as fd:
        fd.write('\n'.join(lines))

    counts = bgsignature.count(mut_file, None, kmer_size=3, genome_build='acgt',
                               collapse=True, includeN=False, group='SAMPLE', cores=None)

    assert len(counts) == 2
    counts_x = counts['X']
    assert len(counts_x) == 4
    assert counts_x['TAC>C'] == 1
    assert counts_x['GTA>G'] == 1
    assert counts_x['ACG>T'] == 1
    assert counts_x['CGT>A'] == 1
    counts_y = counts['Y']
    assert len(counts_y)
    assert counts_y['ACG>T'] == 1
    assert counts_y['CGT>A'] == 1


def test_n(tmpdir):
    """Test with N nucleotides"""
    lines = ['\t'.join(['CHR', 'POS', 'REF', 'ALT'])]
    lines.append('\t'.join(['1', '6', 'A', 'C']))
    lines.append('\t'.join(['1', '7', 'C', 'T']))
    lines.append('\t'.join(['1', '8', 'G', 'T']))
    lines.append('\t'.join(['1', '9', 'T', 'A']))

    mut_file = path.join(str(tmpdir), 'mut.tsv')
    with open(mut_file, 'w') as fd:
        fd.write('\n'.join(lines))

    # exclude Ns
    counts = bgsignature.count(mut_file, None, kmer_size=3, genome_build='acgtn',
                               collapse=False, includeN=False, group=None, cores=None)

    assert len(counts) == 2
    assert counts['ACG>T'] == 1
    assert counts['CGT>T'] == 1

    # include Ns
    counts = bgsignature.count(mut_file, None, kmer_size=3, genome_build='acgtn',
                               collapse=False, includeN=True, group=None, cores=None)

    assert len(counts) == 4
    assert counts['NAC>C'] == 1
    assert counts['ACG>T'] == 1
    assert counts['CGT>T'] == 1
    assert counts['GTN>A'] == 1


def test_5mer(tmpdir):
    """Simple test of a mutations file using pentamers"""
    lines = ['\t'.join(['CHR', 'POS', 'REF', 'ALT'])]
    lines.append('\t'.join(['1', '5', 'A', 'C']))
    lines.append('\t'.join(['1', '6', 'C', 'T']))

    mut_file = path.join(str(tmpdir), 'mut.tsv')
    with open(mut_file, 'w') as fd:
        fd.write('\n'.join(lines))

    counts = bgsignature.count(mut_file, None, kmer_size=5, genome_build='acgt',
                               collapse=False, includeN=False, group=None, cores=None)

    assert len(counts) == 2
    assert counts['GTACG>C'] == 1
    assert counts['TACGT>T'] == 1
