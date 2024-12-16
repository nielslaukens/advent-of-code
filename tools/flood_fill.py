import typing


def adjacent_positions(location: tuple[int, ...]) -> typing.Generator[tuple[int, ...], None, None]:
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


def flood_fill(
        grid: typing.Callable[[tuple[int, ...]], typing.Any],
        start_position: tuple[int, ...],
        filled: set[tuple[int, ...]] = None,
) -> set[tuple[int, ...]]:
    """
    :param grid: Called to get the value at a given location. Should raise IndexError if out of bounds
    :param start_position:
    """
    if filled is None:
        filled: set[tuple[int, ...]] = set()
    filled.add(start_position)
    value = grid(start_position)
    for neighbour in adjacent_positions(start_position):
        if neighbour in filled:
            continue
        try:
            neighbour_value = grid(neighbour)
        except IndexError:
            continue
        if neighbour_value == value:
            filled.union(flood_fill(grid, neighbour, filled))
    return filled


def nested_array_func(array: list) -> typing.Callable[[tuple[int, ...]], typing.Any]:
    def get_element(loc: tuple[int, ...]) -> typing.Any:
        p = array
        for dim in range(len(loc)):
            if 0 <= loc[dim] < len(p):
                p = p[loc[dim]]
            else:
                raise IndexError()
        return p
    return get_element


if __name__ == "__main__":
    assert set(adjacent_positions((5,))) == {(4,), (6,)}
    assert set(adjacent_positions((5, 10))) == {(4, 10), (6, 10), (5, 9), (5, 11)}
    assert set(adjacent_positions((0, 0, 0))) == {(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)}

    grid = [[0, 1, 0],
            [1, 1, 1],
            [0, 1, 0]]
    grid_l = nested_array_func(grid)
    assert flood_fill(grid_l, (0, 0)) == {(0, 0)}
    assert flood_fill(grid_l, (0, 1)) == {(0, 1), (1, 1), (1, 0), (2, 1), (1, 2)}
