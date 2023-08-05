import logging

from bgsignature.error import BGSignatureError
from bgsignature import load, file
from bgsignature.count import mutation, region

logger = logging.getLogger(__name__)


def check_params(mutations_file, regions_file, kmer_size):
    if mutations_file is None and regions_file is None:
        raise BGSignatureError('Missing input')
    if kmer_size < 3 or kmer_size % 2 == 0:
        raise BGSignatureError('Invalid k-mer size')


def _count(mutations_file, regions_file, kmer_size, genome_build, includeN=False, group=None, cores=None):

    check_params(mutations_file, regions_file, kmer_size)

    # Identify the counting module (count regions or mutations)
    if mutations_file is not None:
        items = load.mutations(mutations_file, regions_file)
        module = mutation
        chuck_size = 10000
    else:
        items = [r for r in load.regions(regions_file)]
        module = region
        if len(items) <= 30:  # few regions are most likely whole chromosomes, and the best is not to group them
            chuck_size = 1
        elif 30 < len(items) < 10**4 and cores is not None:  # make even groups
            chuck_size = len(items) // cores
        else:
            chuck_size = 10**5
    return module.count(items, genome=genome_build, size=kmer_size, includeN=includeN,
                        group=group, cores=cores, chunk=chuck_size)


def count(mutations_file, regions_file, kmer_size, genome_build, collapse=True, includeN=False, group=None, cores=None):
    """
    Count k-mers in regions or from mutations

    If both, mutations and regions, are provided only mutations that map to the regions
    are used.

    Args:
        mutations_file:
        regions_file:
        kmer_size: size of the k-mer to count
        genome_build: build of the reference genome to use
        collapse (flag, optional): whether to join together reverse complementaries or not.
          Default: collapsed
        includeN (flag, optional): whether to include or exclude k-mers with N nucleotides.
          Default: excluded
        group (str, optional): key to be used to group the counts.
          Default: no grouping
        cores (int, optional): number of cores to use for paralelization.
          Default: no parallelization.

    Returns:
        dict. Values are counts and keys are tuples with ref and alt for mutations
        (e.g. 'AAA>C') and string for regions (e.g. 'AAA')

    """
    counts = _count(mutations_file, regions_file, kmer_size, genome_build, includeN=includeN, group=group, cores=cores)

    return counts.collapse() if collapse else counts


def relative_frequency(mutations_file, regions_file, kmer_size, genome_build, collapse=True, includeN=False, group=None, cores=None):
    """
    After computing the counts make the values sum to 1.
    """
    counts = count(mutations_file, regions_file, kmer_size, genome_build, collapse=collapse, includeN=includeN, group=group, cores=cores)
    return counts.sum1()


def normalize(mutations_file, regions_file, kmer_size, genome_build, normalize_file=None, collapse=True, includeN=False, group=None, cores=None):
    """
    After making the counts, divide the counts by other counts in a normalization file
    and make the result sum to 1.

    The normalize_file parameter is optional. If not provided, the counts from
    the regions are used.

    """
    if normalize_file is None:
        if regions_file is None:
            raise BGSignatureError('Missing normalization file')
        else:
            normalization_counts = count(None, regions_file, kmer_size, genome_build, collapse=collapse, includeN=includeN, cores=cores)
    else:
        normalization_counts = file.load(normalize_file)

    counts = count(mutations_file, regions_file, kmer_size, genome_build, collapse=collapse, includeN=includeN, group=group, cores=cores)
    return counts.normalize(normalization_counts)


# TODO add the deconstruct sigs features
