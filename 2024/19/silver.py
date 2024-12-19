import dataclasses
import enum
import time
import typing

from tools.tree import TraverseTreeDepthFirstPost


class Color(enum.Enum):
    White = 'w'
    Blue = 'u'
    Black = 'b'
    Red = 'r'
    Green = 'g'


designs = []
with open("input.txt", "r") as f:
    towels = [
        towel.strip()
        for towel in f.readline().strip().split(',')
    ]
    empty_line = f.readline()
    assert empty_line == "\n"
    for design in f:
        design = design.strip()
        designs.append(design)

print(towels)
print(designs)


sequence_cache: dict[str, list[str] | None] = {}


@dataclasses.dataclass
class State:
    towel_sequence: list[str]
    seq: str
    design: str

    def remaining_design(self) -> str:
        return self.design[len(self.seq):]

    def branches(self) -> typing.Generator["State", None, None]:
        rem_seq = self.remaining_design()
        if rem_seq in sequence_cache:
            if sequence_cache[rem_seq] is None:
                # not possible, stop here
                return
            else:
                # return *A* path, don't walk entire tree
                yield sequence_cache[rem_seq]
                return
        for towel in towels:
            new_seq = self.seq + towel
            if new_seq == self.design[0:len(new_seq)]:
                yield State(
                    [*self.towel_sequence, towel],
                    new_seq,
                    self.design,
                )

    def pretty_print(self) -> str:
        seq = ''
        color = 0
        for towel in self.towel_sequence:
            if color:
                seq += "\033[91m" + towel + "\033[0m"
            else:
                seq += "\033[92m" + towel + "\033[0m"
            color = 1 - color
        return seq


designs_possible = 0
for design in designs:
    it = TraverseTreeDepthFirstPost(State([], '', design), lambda n: n.branches())
    for towel_sequence in it:
        seq = ''.join(towel_sequence.towel_sequence)
        if seq == design:
            print(f"Design {design} is possible: {towel_sequence.pretty_print()}")
            designs_possible += 1
            break
        # else:
        # If we're here, this means that we're not at a leaf-node:
        #   - Non-matching branches are not returned
        #   - Matching branches would have been handled by the above if-clause
        # We are thus at an intermediate node in Post-order
        # None of the branches taken from here were able to form the rest of the design
        # print(f"XX: {design}\n"
        #       f"    {towel_sequence.pretty_print()}  {towel_sequence.remaining_design()}\n")
        sequence_cache[towel_sequence.remaining_design()] = None
    else:
        print(f"Design {design} is NOT possible")

print(f"{designs_possible} designs possible")
