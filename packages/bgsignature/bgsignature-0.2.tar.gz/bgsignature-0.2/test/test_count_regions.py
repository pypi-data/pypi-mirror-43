from . import reference

from os import path

import bgsignature


def test_simple(tmpdir):
    """Single region"""
    lines = ['\t'.join(['CHR', 'START', 'END', 'ELEMENT', 'SYMBOL'])]
    lines.append('\t'.join(['1', '5', '8', 'GENE1', 'SYMBOL1']))

    reg_file = path.join(str(tmpdir), 'reg.tsv')
    with open(reg_file, 'w') as fd:
        fd.write('\n'.join(lines))

    counts = bgsignature.count(None, reg_file, kmer_size=3, genome_build='acgt',
                               collapse=False, includeN=False, group=None, cores=None)

    assert len(counts) == 4
    assert counts['TAC'] == 1
    assert counts['ACG'] == 1
    assert counts['CGT'] == 1
    assert counts['GTA'] == 1


def test_collapse(tmpdir):
    """Collapse kmers"""
    lines = ['\t'.join(['CHR', 'START', 'END', 'ELEMENT', 'SYMBOL'])]
    lines.append('\t'.join(['1', '5', '8', 'GENE1', 'SYMBOL1']))

    reg_file = path.join(str(tmpdir), 'reg.tsv')
    with open(reg_file, 'w') as fd:
        fd.write('\n'.join(lines))

    counts = bgsignature.count(None, reg_file, kmer_size=3, genome_build='acgt',
                               collapse=True, includeN=False, group=None, cores=None)

    assert len(counts) == 4
    assert counts['TAC'] == 2
    assert counts['ACG'] == 2
    assert counts['CGT'] == 2
    assert counts['GTA'] == 2


def test_group(tmpdir):
    """Group mutations by sample"""
    lines = ['\t'.join(['CHR', 'START', 'END', 'ELEMENT', 'SYMBOL'])]
    lines.append('\t'.join(['1', '5', '8', 'GENE1', 'SYMBOL1']))
    lines.append('\t'.join(['1', '5', '8', 'GENE2', 'SYMBOL2']))

    reg_file = path.join(str(tmpdir), 'reg.tsv')
    with open(reg_file, 'w') as fd:
        fd.write('\n'.join(lines))

    counts = bgsignature.count(None, reg_file, kmer_size=3, genome_build='acgt',
                               collapse=False, includeN=False, group='SYMBOL', cores=None)

    assert len(counts) == 2
    for k, v in counts.items():
        assert k.startswith('SYMBOL')
        assert v['TAC'] == 1
        assert v['ACG'] == 1
        assert v['CGT'] == 1
        assert v['GTA'] == 1


def test_group_collapse(tmpdir):
    """Group mutations by sample and collapse"""
    lines = ['\t'.join(['CHR', 'START', 'END', 'ELEMENT', 'SYMBOL'])]
    lines.append('\t'.join(['1', '5', '8', 'GENE1', 'SYMBOL1']))
    lines.append('\t'.join(['1', '5', '8', 'ELEMENT2', 'SYMBOL2']))

    reg_file = path.join(str(tmpdir), 'reg.tsv')
    with open(reg_file, 'w') as fd:
        fd.write('\n'.join(lines))

    counts = bgsignature.count(None, reg_file, kmer_size=3, genome_build='acgt',
                               collapse=True, includeN=False, group='SYMBOL', cores=None)

    assert len(counts) == 2
    for k, v in counts.items():
        assert k.startswith('SYMBOL')
        assert v['TAC'] == 2
        assert v['ACG'] == 2
        assert v['CGT'] == 2
        assert v['GTA'] == 2


def test_n(tmpdir):
    """Test including N nucleotides"""
    lines = ['\t'.join(['CHR', 'START', 'END', 'ELEMENT', 'SYMBOL'])]
    lines.append('\t'.join(['1', '6', '9', 'GENE1', 'SYMBOL1']))

    reg_file = path.join(str(tmpdir), 'reg.tsv')
    with open(reg_file, 'w') as fd:
        fd.write('\n'.join(lines))

    counts = bgsignature.count(None, reg_file, kmer_size=3, genome_build='acgtn',
                               collapse=False, includeN=True, group=None, cores=None)

    print(counts)
    assert len(counts) == 4
    assert counts['NAC'] == 1
    assert counts['ACG'] == 1
    assert counts['CGT'] == 1
    assert counts['GTN'] == 1


def test_n_exclude(tmpdir):
    """Test excluding N nucleotides"""
    lines = ['\t'.join(['CHR', 'START', 'END', 'ELEMENT', 'SYMBOL'])]
    lines.append('\t'.join(['1', '6', '9', 'GENE1', 'SYMBOL1']))

    reg_file = path.join(str(tmpdir), 'reg.tsv')
    with open(reg_file, 'w') as fd:
        fd.write('\n'.join(lines))

    counts = bgsignature.count(None, reg_file, kmer_size=3, genome_build='acgtn',
                               collapse=False, includeN=False, group=None, cores=None)

    print(counts)
    assert len(counts) == 2
    assert counts['ACG'] == 1
    assert counts['CGT'] == 1


def test_5mer(tmpdir):
    """Simple test of a mutations file using pentamers"""
    lines = ['\t'.join(['CHR', 'START', 'END', 'ELEMENT', 'SYMBOL'])]
    lines.append('\t'.join(['1', '5', '8', 'GENE1', 'SYMBOL1']))

    reg_file = path.join(str(tmpdir), 'reg.tsv')
    with open(reg_file, 'w') as fd:
        fd.write('\n'.join(lines))

    counts = bgsignature.count(None, reg_file, kmer_size=5, genome_build='acgt',
                               collapse=False, includeN=False, group=None, cores=None)

    assert len(counts) == 4
    assert counts['GTACG'] == 1
    assert counts['TACGT'] == 1
    assert counts['ACGTA'] == 1
    assert counts['CGTAC'] == 1
