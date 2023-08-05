
import collections

from bgsignature.count import SignatureCounter, GroupSignatureCounter
from bgsignature.count.utils import count as base_count
from bgsignature.reference import get_reg, reverse_complementary
from bgsignature.utils import slicing_window


def _read(reg, genome, size):
    chr_ = reg['CHROMOSOME']
    start = reg['START']
    stop = reg['END']
    seq = get_reg(genome, chr_, start, stop, size=size)
    return seq


class Counter(SignatureCounter, collections.Counter):

    def collapse(self):
        reverse_counter = Counter({reverse_complementary(k): v for k, v in self.items()})
        return self + reverse_counter


def count_all(regions, genome, size, includeN=False):
    counter = Counter()
    for reg in regions:
        seq = _read(reg, genome, size)
        if includeN:
            counter_seq = Counter(slicing_window(seq, size))
        else:
            counter_seq = Counter((s for s in slicing_window(seq, size) if 'N' not in s))
        counter += counter_seq
    return counter


class GroupCounter(GroupSignatureCounter):

    def __missing__(self, key):
        self[key] = Counter()
        return self[key]


def count_group(regions, genome, size, group, includeN=False):
    counter = GroupCounter()
    for reg in regions:
        seq = _read(reg, genome, size)
        key = reg[group]
        if includeN:
            counter_seq = Counter(slicing_window(seq, size))
        else:
            counter_seq = Counter((s for s in slicing_window(seq, size) if 'N' not in s))
        counter[key] += counter_seq
    return counter


def count(regions, genome, size=3, includeN=False, group=None, cores=None, chunk=10000):
    return base_count(count_all, Counter, count_group, GroupCounter,
                      regions, genome, size=size, includeN=includeN, group=group,
                      cores=cores, chunk=chunk)
