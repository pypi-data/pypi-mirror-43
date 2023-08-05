"""Utilities related to loading region and mutation files"""


import logging
from collections import defaultdict

from bgcache import bgcache
from bgparsers import readers
from intervaltree import IntervalTree


logger = logging.getLogger(__name__)


def build_regions_tree(regions):

    logger.info('Building regions tree')
    regions_tree = defaultdict(IntervalTree)
    i = 0
    for i, r in enumerate(regions):

        if i % 7332 == 0:
            logger.debug("[%d]", i+1)

        regions_tree[r['CHROMOSOME']].addi(r['START'], r['END']+1)
    logger.debug("Tree done")
    return regions_tree


@bgcache
def load_regions_tree(file):
    regions_ = readers.elements(file)
    return build_regions_tree(regions_)


def mutations(file, regions_file=None):
    """Read mutations.
    If a regions file is provided, only mutations that map to the regions
    are returned"""
    regions_tree = None if regions_file is None else load_regions_tree(regions_file)

    for row in readers.variants(file, extra=['SAMPLE', 'CANCER_TYPE', 'SIGNATURE'],
                                required=['CHROMOSOME', 'POSITION', 'REF', 'ALT']):

        # Get only SNP
        if row['ALT_TYPE'] != 'snp':
            continue

        # Get only mutations in the region of interest
        if regions_tree is None or regions_tree[row['CHROMOSOME']][row['POSITION']]:
            yield row


def regions(file):
    """Read regions file"""
    return readers.elements(file, required=['CHROMOSOME', 'START', 'END'],
                            extra=['ELEMENT', 'SYMBOL'])
