import math

import numpy as np


def lcm_with_offset(period_1: int, offset_1: int, period_2: int, offset_2: int) -> tuple[int, int]:
    # https://math.stackexchange.com/a/3864593
    """
    Similar to Least Common Multiple:
    Calculates N > 0 and M > 0 so that
    N * period_1 - offset_1 = M * period_2 - offset_2.
    """
    gcd, s, t = extended_gcd(period_1, period_2)
    z, rem = divmod(offset_1 - offset_2, gcd)
    if rem != 0:
        raise ValueError("Not possible")

    if z == 0:
        return period_2 // gcd, period_1 // gcd

    n = (z * s) % (period_2 // gcd)
    m = (-z * t) % (period_1 // gcd)
    return n, m


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Extended Greatest Common Divisor Algorithm

    Returns:
        gcd: The greatest common divisor of a and b.
        s, t: Coefficients such that s*a + t*b = gcd

    Reference:
        https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode
    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        quotient, remainder = divmod(old_r, r)
        old_r, r = r, remainder
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


def extended_lcm(a: int, b: int) -> tuple[int, int, int]:
    """
    Returns the least common multiple of a and b, as well as the factors:
    Returns lcm, k and l such that
    k * a + l * b = lcm
    """
    lcm = math.lcm(a, b)
    return lcm, lcm//a, lcm//b


def linear_diophantine(a: int, b: int, c: int) -> tuple[int, int, int, int]:
    """
    Finds `k` and `l` such that k*a + l*b = c

    Note that there are infinitely many (k, l)s: (k + N*i, l - N*j)
    This function returns (k, l, i, j) for the smallest positive k and l
    """
    gcd, s, t = extended_gcd(a, b)
    scale, rem = divmod(c, gcd)
    if rem != 0:
        raise ValueError(f"Not possible: c % gcd(a, b) != 0, {c} % {gcd} = {rem}")
    k, l = s * scale, t * scale

    lcm, i, j = extended_lcm(a, b)
    # try to get positive integers, may fail
    if k < 0:
        n = -(k // i)
        k, l = k + n*i, l - n*j
    if l < 0:
        n = -(l // j)
        k, l = k - n*i, l + n*j
    assert k*a + l*b == c
    assert (k+i)*a + (l-j)*b == c
    return k, l, i, j


if __name__ == "__main__":
    assert lcm_with_offset(3, 0, 5, 1) == (3, 2)
    assert lcm_with_offset(3, 1, 5, 0) == (2, 1)
    assert lcm_with_offset(3, -1, 5, 0) == (3, 2)

    assert extended_gcd(10, 35) == (5, -3, 1)
    assert extended_lcm(10, 25) == (50, 5, 2)

    assert linear_diophantine(3, 4, 11)[0:2] == (1, 2)
