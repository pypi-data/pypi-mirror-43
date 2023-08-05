import functools
import logging

from bgsignature.utils import sum_parallel


def count(count_function, counter_class, count_group_function, counter_group_class,
          items, genome, size=3, includeN=False, group=None, cores=None, chunk=1000):
    """This function acts a decision point to select which is the appropiate function to
    be used, and whether to compute in parallel or not"""

    # Identify the function to be used (count or group count)
    if group is None:
        function = functools.partial(count_function, genome=genome, size=size, includeN=includeN)
        empty = counter_class()
    else:
        function = functools.partial(count_group_function, genome=genome, size=size, group=group, includeN=includeN)
        empty = counter_group_class()

    logging.getLogger('bgsignature').info('Computing counts...')

    # Identify the execution type (serial or parallel)
    if cores is None:
        counts = function(items)
    else:
        counts = sum_parallel(function, items, empty, chunk, cores)
    return counts
