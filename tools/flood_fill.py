import typing

from tools.tuple_tools import adjacent_positions, nested_array_func


def flood_fill(
        grid: typing.Callable[[tuple[int, ...]], typing.Any],
        start_position: tuple[int, ...],
        filled: set[tuple[int, ...]] = None,
) -> set[tuple[int, ...]]:
    """
    Fill a grid by starting at `start_position` and expanding to grid locations
    that have the same value as `grid(start_position)`.
    :param grid: Called to get the value at a given location. Should raise
                 IndexError if out of bounds
    :param start_position: Coordinates to start from
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


if __name__ == "__main__":
    grid = [[0, 1, 0],
            [1, 1, 1],
            [0, 1, 0]]
    grid_l = nested_array_func(grid)
    assert flood_fill(grid_l, (0, 0)) == {(0, 0)}
    assert flood_fill(grid_l, (0, 1)) == {(0, 1), (1, 1), (1, 0), (2, 1), (1, 2)}
