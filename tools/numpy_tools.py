import re
import typing

import numpy


def ndarray_auto_extending_assign(array: numpy.ndarray, coords: typing.Tuple, value, fill=0) -> numpy.ndarray:
    if len(coords) != len(array.shape):
        raise ValueError(f"Need {len(array.shape)}-tuple coordinate, but got {len(coords)}")
    for dim in range(len(array.shape)):
        if array.shape[dim] <= coords[dim]:
            s = list(array.shape)
            s[dim] = coords[dim] - s[dim] + 1
            fill_ar = fill * numpy.ones(shape=s, dtype=array.dtype)
            array = numpy.concatenate((array, fill_ar), axis=dim)
    array[coords] = value
    return array


def str_highlight_value(array, value) -> str:
    s = str(array)
    def highlight(s: str) -> str:
        return f'\033[91m{s}\033[0m'
    return re.sub(f'\\b({value})\\b', lambda m: highlight(m.group(1)), s)
