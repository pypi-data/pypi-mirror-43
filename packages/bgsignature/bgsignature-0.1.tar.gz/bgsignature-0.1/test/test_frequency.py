
from bgsignature.count import mutation, region


def build_mut_counter():
    counter = mutation.Counter()
    counter['AAA>C'] = 2
    counter['AAA>T'] = 1
    counter['CCC>G'] = 1
    return counter


def check_mut_counter(rel_freq_counter):
    assert rel_freq_counter['AAA>C'] == 0.5
    assert rel_freq_counter['AAA>T'] == 0.25
    assert rel_freq_counter['CCC>G'] == 0.25


def build_reg_counter():
    counter = region.Counter()
    counter['AAA'] = 2
    counter['ATA'] = 1
    counter['CCC'] = 1
    return counter


def check_reg_counter(rel_freq_counter):
    assert rel_freq_counter['AAA'] == 0.5
    assert rel_freq_counter['ATA'] == 0.25
    assert rel_freq_counter['CCC'] == 0.25


def test_mut_counter():
    counter = build_mut_counter()
    rfreq = counter.sum1()
    check_mut_counter(rfreq)


def test_reg_counter():
    counter = build_reg_counter()
    rfreq = counter.sum1()
    check_reg_counter(rfreq)


def test_mut_group_counter():
    counter = mutation.GroupCounter()
    counter['GEN1'] = build_mut_counter()
    counter['GEN2'] = build_mut_counter()
    rfreq = counter.sum1()
    assert len(rfreq) == 2
    for k, v in rfreq.items():
        assert k in ['GEN1', 'GEN2']
        check_mut_counter(v)


def test_reg_mut_counter():
    counter = region.GroupCounter()
    counter['GEN1'] = build_reg_counter()
    counter['GEN2'] = build_reg_counter()
    rfreq = counter.sum1()
    assert len(rfreq) == 2
    for k, v in rfreq.items():
        assert k in ['GEN1', 'GEN2']
        check_reg_counter(v)
