import typing

NTuple = typing.TypeVar('NTuple', bound=tuple[int, ...])


def tuple_add(a: NTuple, b: NTuple) -> NTuple:
    """
    Add two tuples as if they were vectors.
    """
    if len(a) != len(b):
        raise ValueError(f"Different number of dimensions: {len(a)} != {len(b)}")
    return tuple(
        a[d] + b[d]
        for d in range(len(a))
    )


def adjacent_positions(location: NTuple) -> typing.Generator[NTuple, None, None]:
    """
    Multi-dimensional adjacency iterator
    :param location: n-tuple of starting coordinates

    Note: may return locations out of bounds of your problem. You still need to bound-check these
    """
    for dimension in range(len(location)):
        yield (
            *location[0:dimension],
            location[dimension] - 1,
            *location[dimension+1:],
        )
        yield (
            *location[0:dimension],
            location[dimension] + 1,
            *location[dimension+1:],
        )


def manhattan_distance(a: NTuple, b: NTuple) -> int:
    """
    Calculate the Manhattan distance between a and b
    """
    if len(a) != len(b):
        raise ValueError(f"Tuples need to have the same length to calculate Manhattan Distance, got {len(a)} and {len(b)}")
    d = 0
    for dimension in range(len(a)):
        d += abs(a[dimension] - b[dimension])
    return d


def positions_within_distance(location: NTuple, steps: int = 1) -> typing.Generator[NTuple, None, None]:
    """
    Multi-dimensional adjacency iterator
    :param location: n-tuple of starting coordinates
    :param steps: maximum number of steps to take (i.e. Manhattan distance from location)

    Note: may return locations out of bounds of your problem. You still need to bound-check these
    """
    if len(location) == 0:
        yield ()
        return
    for i in range(-steps, steps + 1):
        for loc_remaining_dim in positions_within_distance(location[1:], steps - abs(i)):
            yield location[0] + i, *loc_remaining_dim


def index_in_range(index: NTuple, size: NTuple) -> bool:
    """
    Multi-dimensional checker if the coordinates are within the size.
    Checks for each dimension `i` if  0 <= index[i] < size[i]
    """
    if len(index) != len(size):
        raise ValueError(f"index and size must have same dimension, got {len(index)} and {len(size)}")
    for dimension in range(len(index)):
        if not 0 <= index[dimension] < size[dimension]:
            return False
    return True


def nested_array_func(array: list) -> typing.Callable[[tuple[int, ...]], typing.Any]:
    """
    Helper function that allows you to index a nested list-of-lists with a tuple.
    """
    def get_element(loc: tuple[int, ...]) -> typing.Any:
        p = array
        for dim in range(len(loc)):
            if 0 <= loc[dim] < len(p):
                p = p[loc[dim]]
            else:
                raise IndexError()
        return p
    return get_element


if __name__ == '__main__':
    assert tuple_add((1, 2), (3, 4)) == (4, 6)

    assert set(adjacent_positions((5,))) == {(4,), (6,)}
    assert set(adjacent_positions((5, 10))) == {(4, 10), (6, 10), (5, 9), (5, 11)}
    assert set(adjacent_positions((0, 0, 0))) == {(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)}
    assert set(positions_within_distance((0, 0, 0), 0)) == {(0, 0, 0)}
    assert set(positions_within_distance((0,), 1)) == {(-1,), (0,), (1,)}

    pos = list(positions_within_distance((0, 0), 2))
    pos_set = set(pos)
    assert len(pos) == len(pos_set)  # check that we don't yield doubles
    assert pos_set == {(0, 0), (-2, 0), (-1, 0), (1, 0), (2, 0), (0, -2), (0, -1), (0, 1), (0, 2), (-1, -1), (-1, 1), (1, -1), (1, 1)}

    assert index_in_range(tuple(), tuple())
    assert index_in_range((0,), (1,))
    assert not index_in_range((0,), (0,))
    assert index_in_range((0, 0, 0), (1, 2, 3))
    assert not index_in_range((0, 0, 3), (1, 2, 3))

    arr = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert nested_array_func(arr)((1, 2)) == 6
