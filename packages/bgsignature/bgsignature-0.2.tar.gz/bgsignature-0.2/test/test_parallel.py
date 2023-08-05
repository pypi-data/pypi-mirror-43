from os import path

from bgparsers import readers

from bgsignature.count import mutation, region

DIR = path.dirname(path.abspath(__file__))

MUTATIONS = list(readers.variants(path.join(DIR, 'datasets', 'muts.tsv')))
REGIONS = list(readers.elements(path.join(DIR, 'datasets', 'regs.tsv')))


def compare_dicts(d1, d2):
    assert len(d1) == len(d2)
    for k in d1:
        assert d1[k] == d2[k]


def test_mutations():
    serial = mutation.count(MUTATIONS, genome='hg19')
    parallel = mutation.count(MUTATIONS, genome='hg19',
                              cores=2, chunk=1)
    # use chunks o 1 to ensure paralelization

    compare_dicts(serial, parallel)


def test_mutations_group():
    serial = mutation.count(MUTATIONS, genome='hg19', group='SAMPLE')
    parallel = mutation.count(MUTATIONS, genome='hg19', group='SAMPLE',
                              cores=2, chunk=1)
    # use chunks o 1 to ensure paralelization

    assert len(serial) == len(parallel)
    for k in serial:
        compare_dicts(serial[k], parallel[k])


def test_regions():
    serial = region.count(REGIONS, genome='hg19')
    parallel = region.count(REGIONS, genome='hg19',
                              cores=2, chunk=1)
    # use chunks o 1 to ensure paralelization

    compare_dicts(serial, parallel)


def test_regions_group():
    serial = region.count(REGIONS, genome='hg19', group='SYMBOL')
    parallel = region.count(REGIONS, genome='hg19', group='SYMBOL',
                              cores=2, chunk=1)
    # use chunks o 1 to ensure paralelization

    assert len(serial) == len(parallel)
    for k in serial:
        compare_dicts(serial[k], parallel[k])
