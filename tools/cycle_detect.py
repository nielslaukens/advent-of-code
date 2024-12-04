import dataclasses
import typing


NO_INITIAL_STATE = object()


@dataclasses.dataclass
class CycleInfo:
    state: typing.Hashable
    first_occurrence: int
    second_occurrence: int

    @property
    def cycle_length(self) -> int:
        return self.second_occurrence - self.first_occurrence


class CycleDetector:
    """
    Keeps track of seen states and scans for cycles.
    A cycle is found when two identical states are seen in the history.
    """
    def __init__(self, initial_state: typing.Hashable = NO_INITIAL_STATE):
        self.history = []
        if initial_state is not NO_INITIAL_STATE:
            self.append(initial_state)

    def append(self, state: typing.Hashable):
        self.history.append(state)

    def scan(self) -> None | CycleInfo:
        last_seen = {}
        for i, state in enumerate(self.history):
            if state in last_seen:
                return CycleInfo(state, last_seen[state], i)
            last_seen[state] = i


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


if __name__ == "__main__":
    cd = CycleDetector()
    cd.append("something")
    cd.append("foo")
    cd.append("bar")
    cd.append("baz")
    cd.append("foo")
    cycle = cd.scan()
    assert cycle.state == "foo"
    assert cycle.first_occurrence == 1
    assert cycle.second_occurrence == 4
    assert cycle.cycle_length == 3

    assert lcm_with_offset(3, 0, 5, 1) == (3, 2)
    assert lcm_with_offset(3, 1, 5, 0) == (2, 1)
    assert lcm_with_offset(3, -1, 5, 0) == (3, 2)
