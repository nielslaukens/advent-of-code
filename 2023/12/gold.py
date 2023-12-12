from __future__ import annotations

import dataclasses
import re


@dataclasses.dataclass
class InsertResult:
    bitmap: list[str]
    inserted_at: int
    next_insert_at_or_after: int


class TristateBitmap:
    def __init__(self, runs: list[tuple[str, int]], desired_hash_runs: list[int]):
        self.runs = runs
        self.desired_hash_runs = desired_hash_runs
        self._bitmap = None

    @classmethod
    def from_bitmap(cls, bitmap: str, desired_hash_runs: list[int]):
        last_ch = None
        last_ch_count = 0
        runs = []
        for ch in bitmap:
            if ch == last_ch:
                last_ch_count += 1
            else:  # ch != last_ch
                if last_ch is not None:
                    runs.append((last_ch, last_ch_count))
                last_ch = ch
                last_ch_count = 1
        if last_ch is not None:
            runs.append((last_ch, last_ch_count))
        o = cls(runs, desired_hash_runs)
        o._bitmap = bitmap
        return o

    @property
    def bitmap(self) -> str:
        if self._bitmap is None:
            self._bitmap = ''
            for run in self.runs:
                self._bitmap += run[0] * run[1]
        return self._bitmap

    def __str__(self) -> str:
        return f"TristateBitmap({self.bitmap!r}, {self.desired_hash_runs})"

    def _runs_from_start(self, start_pos: int) -> list[tuple[list[str], int]]:
        """
        Filter self.runs to start from start_pos
        """
        p = 0
        filtered_runs = list(self.runs)
        while p < start_pos:
            if p + filtered_runs[0][1] <= start_pos:
                p += filtered_runs[0][1]
                filtered_runs.pop(0)
            else:  # partial match
                filtered_runs[0] = (filtered_runs[0][0], filtered_runs[0][1] - start_pos)
                p = start_pos
        return filtered_runs

    @staticmethod
    def try_insert_old(bitmap: list[str], run: int, start_pos: int = 0) -> InsertResult | None:
        if start_pos + run > len(bitmap):
            return None

        for i in range(start_pos):
            if bitmap[i] == '?':
                bitmap[i] = '.'

        for i in range(start_pos, len(bitmap)-run+1):
            if all(map(lambda j: bitmap[i+j] in ["#", "?"], range(run))):
                match_at_start = i == 0
                match_at_end = i + run == len(bitmap)
                if (match_at_start or bitmap[i - 1] in ['?', '.']) and \
                        (match_at_end or bitmap[i + run] in ["?", "."]):
                    if not match_at_start:
                        assert bitmap[i-1] in ['.', '?']
                        bitmap[i-1] = '.'
                    for j in range(run):
                        assert bitmap[i+j] in ['#', '?']
                        bitmap[i+j] = '#'
                    if not match_at_end:
                        assert bitmap[i + run] in ['.', '?']
                        bitmap[i + run] = '.'
                    return InsertResult(
                        bitmap=bitmap,
                        inserted_at=i,
                        next_insert_at_or_after=i + run + 1,
                    )

        return None

    @staticmethod
    def try_insert(bitmap: list[str], run: int, start_pos: int = 0) -> InsertResult | None:
        bitmap = ''.join(bitmap)
        pattern = r'([.?]*?)(' + ("[#?]"*run) + r')([.?]|$)'
        m = re.match(pattern, bitmap[start_pos:])
        if m is None:
            return None
        bitmap = list(bitmap)
        if m.group(1) != "":
            bitmap[(start_pos+m.start(1)):(start_pos+m.end(1))] = ["."] * len(m.group(1))
        bitmap[(start_pos+m.start(2)):(start_pos+m.end(2))] = ["#"] * run
        if m.group(3) != "":
            bitmap[start_pos+m.start(3)] = "."
        return InsertResult(
            bitmap=bitmap,
            inserted_at=start_pos+m.start(2),
            next_insert_at_or_after=start_pos+m.end(0),
        )

    def possibilities(self) -> int:
        return self._possibilities(bitmap=list(self.bitmap), start_pos=0, to_place=list(self.desired_hash_runs))

    @staticmethod
    def _possibilities(bitmap: list[str], start_pos: int = 0, to_place: list[int] = None) -> int:
        if len(to_place) == 0:
            #print(f"{''.join(bitmap)} => match")
            return 1

        if bitmap[start_pos:].count('#') > sum(to_place):
            # there are more defective springs left than we need to place,
            # invalid chain
            return 0

        to_place_now = to_place.pop(0)

        possibilities = 0
        i = start_pos
        while i < len(bitmap):
            insert = TristateBitmap.try_insert(list(bitmap), to_place_now, i)
            if insert is None:
                break
            #print(f"try_insert({''.join(bitmap)}, [{to_place_now}, {to_place}], {i}) => {''.join(insert.bitmap)}")
            p = TristateBitmap._possibilities(insert.bitmap, insert.next_insert_at_or_after, list(to_place))
            possibilities += p

            if bitmap[insert.inserted_at] == '#':  # can't move this run
                break
            i = insert.inserted_at + 1

        return possibilities


spring_rows: list[TristateBitmap] = []
with open("input.txt", "r") as f:
    for line in f:
        line = line.rstrip()
        bitmap, cont_gr = line.split()
        cont_gr = [int(_) for _ in cont_gr.split(',')]
        # unfold
        bitmap = '?'.join([bitmap] * 5)
        cont_gr = cont_gr * 5
        spring_rows.append(TristateBitmap.from_bitmap(bitmap, cont_gr))


total_possibilities = 0
for row in spring_rows:
    print(f"{row}  =>  ", end="")
    p = row.possibilities()
    print(f"{p}")
    total_possibilities += p

print(total_possibilities)
