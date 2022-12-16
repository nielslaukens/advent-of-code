from __future__ import annotations


import typing


class Slices:
    """
    Combine a list of slice()s
    """
    def __init__(self, ranges: typing.Iterable[slice] = None):
        if ranges is None:
            ranges = []

        self._ranges: list[slice] = []

        for range in ranges:
            self.__iadd__(range)

    @staticmethod
    def _add_slices(a: slice, b: slice) -> list[slice]:
        """
        Join slices a and b.
        If a and b (partially) overlap, only a single slice will be returned
        """
        if a.start == a.stop:
            # a is empty
            return [b]
        if b.start == b.stop:
            # b is empty
            return [a]

        if a.start > b.start:
            b, a = a, b
        assert a.start <= b.start
        if a.stop < b.start:
            # no overlap
            return [a, b]
        if b.stop <= a.stop:
            # a completely encompasses b
            return [a]
        if a.start <= b.start <= a.stop <= b.stop:
            # b extends a
            return [slice(a.start, b.stop)]
        raise NotImplementedError(f"Don't know how to join [{a.start}, {a.stop}) "
                                  f"with [{b.start},{b.stop})")

    @staticmethod
    def _remove_slice(base: slice, cut_out: slice) -> list[slice]:
        """
        Removes `cut_out` from `base`.
        """
        if cut_out.start == cut_out.stop:
            # cut_out is empty
            return [base]
        if cut_out.stop <= base.start:
            # cut_out is before base
            return [base]
        if base.stop <= cut_out.start:
            # cut_out is after base
            return [base]
        if cut_out.start <= base.start <= base.stop <= cut_out.stop:
            # cut_out cuts everything
            return []
        if cut_out.start <= base.start <= cut_out.stop <= base.stop:
            # cut_out cuts a piece from the start
            return [slice(cut_out.stop, base.stop)]
        if base.start <= cut_out.start <= cut_out.stop <= base.stop:
            # cut_out cuts a piece from the middle
            return [slice(base.start, cut_out.start),
                    slice(cut_out.stop, base.stop)]
        if base.start <= cut_out.start <= base.stop <= cut_out.stop:
            # cut_out cuts a piece from the end
            return [slice(base.start, cut_out.start)]
        raise NotImplementedError(
            f"Don't know how to cut [{cut_out.start},{cut_out.stop}) "
            f"from [{base.start},{base.stop})")


    def add(self, other: Slices | slice) -> typing.Self:
        self.__iadd__(other)
        return self

    def __iadd__(self, other: Slices | slice) -> None:
        if isinstance(other, Slices):
            for range in other._ranges:
                self.__iadd__(range)

        elif isinstance(other, slice):
            if not (other.step is None or other.step == 1):
                raise ValueError(f"Only slices with step=1 are supported. Got: {repr(other)}")

            if other.start == other.stop:
                return

            new_ranges = sorted([*self._ranges, other], key=lambda item: item.start)
            self._ranges = [new_ranges.pop(0)]
            for new_range in new_ranges:
                prev = self._ranges.pop(-1)
                r = self._add_slices(prev, new_range)
                self._ranges.extend(r)

        else:
            raise ValueError(f"Unknown type {other.__class__}")

    def remove(self, other: Slices | slice) -> typing.Self:
        self.__isub__(other)
        return self

    def __isub__(self, other: Slices | slice) -> None:
        if isinstance(other, Slices):
            for range in other._ranges:
                self.__isub__(range)

        elif isinstance(other, slice):
            if not (other.step is None or other.step == 1):
                raise ValueError(f"Only slices with step=1 are supported. Got: {repr(other)}")

            if other.start == other.stop:
                return

            range_to_remove = []
            range_to_add = []
            for i, range in enumerate(self._ranges):
                if other.stop <= range.start:
                    # ranges are sorted; we're past the location where an existing range could have been
                    break
                elif range.stop <= other.start:
                    pass  # not there yet, go to next range
                elif other.start <= range.start and range.stop <= other.stop:
                    # to-remove encompasses range completely
                    range_to_remove.append(i)  # can't be done in-loop; note for later
                elif other.start <= range.start < other.stop < range.stop:
                    # Remove from start
                    self._ranges[i] = slice(other.stop, range.stop)
                elif range.start < other.start < range.stop <= other.stop:
                    # remove from end
                    self._ranges[i] = slice(range.start, other.start)
                elif range.start < other.start < other.stop < range.stop:
                    # cuts from the middle
                    range_to_remove.append(i)
                    range_to_add.append((i, slice(range.start, other.start)))
                    range_to_add.append((i+1, slice(other.stop, range.stop)))
                    break
                else:
                    raise NotImplementedError(f"can't remove {other.start}-{other.stop} from {range.start}-{range.stop}")
            for i in reversed(range_to_remove):
                # reversed, so the indices don't change
                del self._ranges[i]
            for i, s in range_to_add:
                self._ranges.insert(i, s)

        else:
            raise ValueError(f"Unknown type {other.__class__}")

    def __repr__(self) -> str:
        c = ", ".join([str(_) for _ in self._ranges])
        return f"Slices([{c}])"

    def __len__(self) -> int:
        l = 0
        for range in self._ranges:
            l += range.stop - range.start
        return l


if __name__ == "__main__":
    assert Slices()._ranges == []
    assert Slices([slice(0, 10)])._ranges == [slice(0, 10)]
    assert Slices([slice(0, 10), slice(10, 20)])._ranges == [slice(0, 20)]
    assert Slices([slice(0, 10), slice(11, 20)])._ranges == [slice(0, 10), slice(11, 20)]
    assert Slices([slice(0, 10), slice(-10, 20)])._ranges == [slice(-10, 20)]

    assert Slices([slice(10, 20)]).remove(slice(10, 20))._ranges == []
    assert Slices([slice(10, 20)]).remove(slice(5, 15))._ranges == [slice(15, 20)]
    assert Slices([slice(10, 20)]).remove(slice(5, 25))._ranges == []
    assert Slices([slice(10, 20)]).remove(slice(15, 25))._ranges == [slice(10, 15)]
    assert Slices([slice(10, 20)]).remove(slice(12, 18))._ranges == [slice(10, 12), slice(18, 20)]
