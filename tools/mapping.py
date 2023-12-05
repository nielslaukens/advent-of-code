"""
Utility classes to store and apply mappings of integer ranges.

The Mapping class stores a set of (source-range -> dest_range) mappings
and provides functionality to map an integer, a range or a list of ranges from source to dest.
"""

import dataclasses

import typing


@dataclasses.dataclass
class Map:
    source_start: int
    dest_start: int
    length: int

    @property
    def source_last(self) -> int:
        return self.source_start + self.length - 1

    @property
    def source_stop(self) -> int:
        return self.source_start + self.length


class Mapping:
    def __init__(self, maps: typing.Iterable[Map] = None):
        if maps is None:
            maps = []

        self.ranges: list[Map] = []

        for m in maps:
            self.add_map(m)

    def add_range(self, dest_start: int, source_start: int, length: int):
        return self.add_map(Map(source_start=source_start, dest_start=dest_start, length=length))

    def add_map(self, new_map: Map):
        i = 0
        for i, m in enumerate(self.ranges):
            if new_map.source_start <= m.source_start:
                break
        else:
            i = len(self.ranges)

        if i > 0 and self.ranges[i-1].source_last > new_map.source_start:
            raise ValueError(f"Overlapping mapping: already have {self.ranges[i-1]}, try to add {new_map}")
        if i < len(self.ranges) and new_map.source_last >= self.ranges[i].source_start:
            raise ValueError(f"Overlapping mapping: try to add {new_map}, already have {self.ranges[i]}")

        self.ranges.insert(i, new_map)

    def __repr__(self) -> str:
        return f"Mapping({self.ranges})"

    def __getitem__(self, item: int) -> int:
        for r in self.ranges:
            if r.source_start <= item < r.source_start + r.length:
                return r.dest_start + (item - r.source_start)
            if item < r.source_start:
                break  # ranges are sorted, we won't find anything anymore
        return item

    def map_slices(self, slice_list: list[slice]) -> list[slice]:
        """
        Map a list of slices through this mapping.
        Note that the returned list of slices may contain overlapping slices
        """
        # The order of iteration is important!
        # We want to iterate over slices first, and for each slice see what mapping apply,
        # otherwise we have a mix of source & destination IDs
        out: list[slice] = []
        for sl in slice_list:
            to_map = sl
            for r in self.ranges:
                if r.source_last < to_map.start:  # range is before current slice
                    continue

                elif r.source_start <= to_map.start < r.source_stop < to_map.stop:
                    # range overlaps start of sl
                    mapped_sl_start = r.dest_start + (to_map.start - r.source_start)
                    mapped_r_stop = r.dest_start + (r.source_stop - r.source_start)
                    out.append(slice(mapped_sl_start, mapped_r_stop))
                    to_map = slice(r.source_stop, to_map.stop)

                elif r.source_start <= to_map.start and to_map.stop <= r.source_stop:
                    # range overlaps entirety of sl
                    mapped_sl_start = r.dest_start + (to_map.start - r.source_start)
                    mapped_sl_stop = r.dest_start + (to_map.stop - r.source_start)
                    out.append(slice(mapped_sl_start, mapped_sl_stop))
                    to_map = None
                    break

                elif to_map.start < r.source_start and r.source_stop < to_map.stop:
                    # range is within sl
                    # Since ranges are sorted, we know that the first part of sl, before range will be identity-mapped
                    out.append(slice(to_map.start, r.source_start))
                    mapped_r_start = r.dest_start + (r.source_start - r.source_start)
                    mapped_r_stop = r.dest_start + (r.source_stop - r.source_start)
                    out.append(slice(mapped_r_start, mapped_r_stop))

                    to_map = slice(r.source_stop, to_map.stop)

                elif to_map.start < r.source_start < to_map.stop <= r.source_stop:
                    # range starts within sl and continues beyond sl's end
                    # Since ranges are sorted, we know that the first part of sl, before range will be identity-mapped
                    out.append(slice(to_map.start, r.source_start))
                    mapped_r_start = r.dest_start + (r.source_start - r.source_start)
                    mapped_sl_stop = r.dest_start + (to_map.stop - r.source_start)
                    out.append(slice(mapped_r_start, mapped_sl_stop))
                    to_map = None
                    break

                elif to_map.stop <= r.source_start:
                    # range is after sl
                    continue

            # identity-map the rest
            if to_map is not None:
                out.append(to_map)

        return out


if __name__ == "__main__":
    m = Mapping([Map(10, 110, 10)])  # 10–19 => 110–119
    assert m[0] == 0
    assert m[9] == 9
    assert m[10] == 110
    assert m[19] == 119
    assert m[20] == 20

    assert m.map_slices([slice(5, 10)]) == [slice(5, 10)]
    assert m.map_slices([slice(5, 11)]) == [slice(5, 10), slice(110, 111)]
    assert m.map_slices([slice(5, 20)]) == [slice(5, 10), slice(110, 120)]
    assert m.map_slices([slice(5, 21)]) == [slice(5, 10), slice(110, 120), slice(20, 21)]
    assert m.map_slices([slice(10, 15)]) == [slice(110, 115)]
    assert m.map_slices([slice(10, 20)]) == [slice(110, 120)]
    assert m.map_slices([slice(10, 21)]) == [slice(110, 120), slice(20, 21)]
    assert m.map_slices([slice(11, 15)]) == [slice(111, 115)]
    assert m.map_slices([slice(11, 20)]) == [slice(111, 120)]
    assert m.map_slices([slice(11, 21)]) == [slice(111, 120), slice(20, 21)]
    assert m.map_slices([slice(19, 20)]) == [slice(119, 120)]
    assert m.map_slices([slice(19, 21)]) == [slice(119, 120), slice(20, 21)]
    assert m.map_slices([slice(20, 21)]) == [slice(20, 21)]
