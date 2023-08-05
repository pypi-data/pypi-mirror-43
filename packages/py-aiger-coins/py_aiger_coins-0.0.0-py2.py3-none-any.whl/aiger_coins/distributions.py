import math
from fractions import Fraction
from functools import reduce

import aiger
import funcy as fn
from aigerbv import atom

from aiger_coins import utils


def _kmodels(var, k, max_val):
    return ~(var ^ var) if k == max_val else var < k


def to_frac(prob):
    prob = Fraction(*prob) if isinstance(prob, tuple) else Fraction(prob)
    assert 0 <= prob <= 1
    return prob


def coin(prob, input_name=None):
    # TODO: reimplement in terms of common_denominator_method.
    prob = to_frac(prob)
    mux, is_valid = mutex_coins({'H': prob, 'T': 1 - prob})
    return mux >> aiger.sink('T'), is_valid


def mutex_coins(name2prob, input_name=None, keep_seperate=False):
    """Mutually exclusive coins.

    Encoded using the common denominator method.
    """
    name2prob = fn.walk_values(to_frac, name2prob)
    assert sum(name2prob.values()) == 1

    bots = [p.denominator for p in name2prob.values()]
    lcm = reduce(utils.lcm, bots, 1)
    word_len = max(math.ceil(math.log2(lcm)), 1)
    max_val = 2**word_len

    name2weight = fn.walk_values(
        lambda p: p.numerator*(lcm // p.denominator),
        name2prob
    )

    bits = atom(word_len, input_name, signed=False)
    const_true = ~(bits @ 0)
    total, coins = 0, []
    for name, weight in name2weight.items():
        lb = const_true if total == 0 else (bits >= total)
        total += weight
        ub = const_true if total == max_val else (bits < total)
        expr = (lb & ub)
        output = dict(expr.aigbv.output_map)[expr.output][0]
        coins.append(expr.aig['o', {output: name}])

    is_valid = const_true if lcm == max_val else bits < lcm

    if keep_seperate:
        return coins, is_valid
    return reduce(lambda x, y: x | y, coins), is_valid
