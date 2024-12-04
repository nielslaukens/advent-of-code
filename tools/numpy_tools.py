import re
import typing

import numpy


def ndarray_auto_extending_assign(array: numpy.ndarray, coords: typing.Tuple, value, fill=0) -> numpy.ndarray:
    """
    Sets array[coords] to value, extending array if needed with fill values
    """
    if len(coords) != len(array.shape):
        raise ValueError(f"Need {len(array.shape)}-tuple coordinate, but got {len(coords)}")
    for dim in range(len(array.shape)):
        if array.shape[dim] <= coords[dim]:
            s = list(array.shape)
            s[dim] = coords[dim] - s[dim] + 1
            fill_ar = numpy.full(shape=s, dtype=array.dtype, fill_value=fill)
            array = numpy.concatenate((array, fill_ar), axis=dim)
    array[coords] = value
    return array


def str_highlight_value(array: numpy.ndarray, value: typing.Union[int, str]) -> str:
    """
    Stringifies the array, but highlights "words" (in regex sense) that match `value`
    """
    s = str(array)
    def highlight(s: str) -> str:
        return f'\033[91m{s}\033[0m'
    return re.sub(f'\\b({value})\\b', lambda m: highlight(m.group(1)), s)


def str_values_only(array: numpy.ndarray) -> str:
    """
    Render the array, but without the '[]'.
    The first dimension is rendered vertically (i.e. indicates the line, or y position, counting down)
    The second dimension is rendered horizontally (i.e. indicating the column, or x position, counting right)
    """
    out = ""
    with numpy.nditer(array, order='C', flags=['multi_index'], op_flags=['readonly']) as it:
        prev_y = 0
        for occ in it:
            if it.multi_index[0] != prev_y:
                prev_y = it.multi_index[0]
                out += "\n"
            out += str(occ)
    return out


def one_d_line(
        arr: numpy.ndarray,
        start_point: tuple | numpy.ndarray,
        length: int,
        direction: tuple | numpy.ndarray,
        start_offset: int = 0,
) -> numpy.ndarray | None:
    """
    Takes elements from `arr`, starting at coordinates `start_point` and taking `direction` steps for a total of
    `length` step.
    Returns None if this would go outside the given array.

    Optionally, the line can start `start_offset` steps from `start_point`
    """
    start_point = numpy.array(start_point)
    direction = numpy.array(direction)
    indices = numpy.array([
        tuple(start_point + (i+start_offset) * direction)
        for i in range(length)
    ])
    for index in indices:
        for dim, size in enumerate(arr.shape):
            if index[dim] < 0 or index[dim] >= size:
                return None

    # now swap indices around. We currently have a list (axis=0) of indices;
    # numpy wants a list *within* each index (i.e. the list should be at axis=N)
    indices = numpy.moveaxis(indices, 0, -1)
    line = arr[tuple(indices.tolist())]
    assert len(line.shape) == 1
    return line


if __name__ == "__main__":
    arr = numpy.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ])
    assert numpy.array_equal(one_d_line(
        arr,
        (0, 0), 3, (1, 1),
    ), numpy.array([1, 5, 9]))
    assert numpy.array_equal(one_d_line(
        arr,
        (1, 1), 2, (-1, -1),
    ), numpy.array([5, 1]))
    assert one_d_line(
        arr,
        (1, 1), 3, (1, 1),
    ) is None
    assert one_d_line(
        arr,
        (1, 1), 3, (-1, -1),
    ) is None
    assert numpy.array_equal(one_d_line(
        arr,
        (1, 1), 3, (1, 1), -1,
    ), numpy.array([1, 5, 9]))
