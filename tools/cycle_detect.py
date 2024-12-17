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
