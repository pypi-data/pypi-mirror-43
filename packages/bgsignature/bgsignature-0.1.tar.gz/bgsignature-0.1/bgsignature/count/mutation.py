import logging

from bgsignature.count import SignatureCounter, GroupSignatureCounter
from bgsignature.count.utils import count as base_count
from bgsignature.reference import get_kmer, reverse_complementary


logger = logging.getLogger(__name__)


def _read(mut, genome, size, includeN=False):
    chr_ = mut['CHROMOSOME']
    pos = mut['POSITION']
    ref = mut['REF']
    alt = mut['ALT']
    kmer = get_kmer(genome, chr_, pos, size=size)
    mid = size // 2
    if kmer[mid] != ref:
        logger.debug('Reference mismatch in mutation %s:%d %s>%s' % (chr_, pos, ref, alt))
        return None
    if not includeN and 'N' in kmer:
        return None
    if alt == ref:
        logger.debug('Mutation has same reference and alternate %s:%d %s>%s' % (chr_, pos, ref, alt))
        return None
    return kmer + '>' + alt


class Counter(SignatureCounter):

    def __missing__(self, key):
        return 0

    def __truediv__(self, other):
        counter = self.__class__()
        for k in self.keys():  # only on left values
            counter[k] = self[k] / other[k[:-2]]  # use the ref k-mer of the mutation only
        return counter

    @staticmethod
    def _reverse_complementary(key):
        seq_ref, alt = key.split('>')
        return reverse_complementary(seq_ref) + '>' + reverse_complementary(alt)

    def collapse(self):
        reverse_counter = Counter()
        for k, v in self.items():
            reverse_counter[Counter._reverse_complementary(k)] = v
        return self + reverse_counter


def count_all(mutations, genome, size, includeN=False):
    counter = Counter()
    for mut in mutations:
        change = _read(mut, genome, size, includeN=includeN)
        if change is None:
            continue
        counter[change] += 1
    return counter


class GroupCounter(GroupSignatureCounter):

    def __missing__(self, key):
        self[key] = Counter()
        return self[key]


def count_group(mutations, genome, size, group, includeN=False):
    counter = GroupCounter()
    for mut in mutations:
        change = _read(mut, genome, size, includeN=includeN)
        if change is None:
            continue
        key = mut[group]
        counter[key][change] += 1
    return counter


def count(mutations, genome, size=3, includeN=False, group=None, cores=None, chunk=10000):
    return base_count(count_all, Counter, count_group, GroupCounter,
                      mutations, genome, size=size, includeN=includeN, group=group,
                      cores=cores, chunk=chunk)
