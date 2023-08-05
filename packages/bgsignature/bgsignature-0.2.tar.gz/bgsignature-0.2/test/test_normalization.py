
from bgsignature.count import mutation, region


def build_mut_counter():
    counter = mutation.Counter()
    counter['AAA>C'] = 2
    counter['ATA>C'] = 1
    counter['CCC>G'] = 1
    return counter


def check_mut_counter(rel_freq_counter):
    assert rel_freq_counter['AAA>C'] == 0.2
    assert rel_freq_counter['ATA>C'] == 0.4
    assert rel_freq_counter['CCC>G'] == 0.4


def build_reg_counter():
    counter = region.Counter()
    counter['AAA'] = 2
    counter['ATA'] = 1
    counter['CCC'] = 1
    return counter


def check_reg_counter(rel_freq_counter):
    assert rel_freq_counter['AAA'] == 0.2
    assert rel_freq_counter['ATA'] == 0.4
    assert rel_freq_counter['CCC'] == 0.4


NORMALIZATION_COUNTS = {'AAA': 20, 'ATA': 5, 'CCC': 5}


def test_mut_counter():
    counter = build_mut_counter()
    n = counter.normalize(NORMALIZATION_COUNTS)
    check_mut_counter(n)


def test_reg_counter():
    counter = build_reg_counter()
    n = counter.normalize(NORMALIZATION_COUNTS)
    check_reg_counter(n)


def test_mut_group_counter():
    counter = mutation.GroupCounter()
    counter['GEN1'] = build_mut_counter()
    counter['GEN2'] = build_mut_counter()
    n = counter.normalize(NORMALIZATION_COUNTS)
    assert len(n) == 2
    for k, v in n.items():
        assert k in ['GEN1', 'GEN2']
        check_mut_counter(v)


def test_reg_mut_counter():
    counter = region.GroupCounter()
    counter['GEN1'] = build_reg_counter()
    counter['GEN2'] = build_reg_counter()
    n = counter.normalize(NORMALIZATION_COUNTS)
    assert len(n) == 2
    for k, v in n.items():
        assert k in ['GEN1', 'GEN2']
        check_reg_counter(v)


def test_independency():
    counter = mutation.Counter()
    counter['AAA>C'] = 2
    counter['AAA>T'] = 8
    for i in range(1, 100):
        normalization_counts = {'AAA': i}
        n = counter.normalize(normalization_counts)
        assert 0.199999999 < n['AAA>C'] < 0.200000001
        assert 0.799999999 < n['AAA>T'] < 0.800000001


def test_same_ref():
    counter = mutation.Counter()
    counter['AAA>C'] = 2
    counter['AAA>T'] = 1
    counter['CCC>G'] = 1
    normalization_counts = {'AAA': 10, 'ATA': 5, 'CCC': 5}
    n = counter.normalize(normalization_counts)
    assert n['AAA>T'] == 0.2
    assert n['AAA>C'] == 0.4
    assert n['CCC>G'] == 0.4


def test_missing():
    counter = build_mut_counter()
    normalization_counts = {'AAA': 20, 'ATA': 5}
    try:
        counter.normalize(normalization_counts)
    except KeyError:
        assert True
    else:
        assert False
