from copy import copy

import numpy as np
import typing


class InfiniteGrid:
    def __init__(self, fill_value: typing.Any = 0, dtype: object | None = None):
        self.fill_value = fill_value
        self._grid = np.full(shape=(0, 0), dtype=dtype, fill_value=fill_value)
        self._offset = None

    @property
    def _x_range(self) -> slice:
        return slice(self._offset[0], self._offset[0] + self._grid.shape[0])

    @property
    def _y_range(self) -> slice:
        return slice(self._offset[1], self._offset[1] + self._grid.shape[1])

    def offset_coord(self, coord: tuple[int | slice, int | slice]) -> tuple[int | slice, int | slice]:
        if self._offset is None:
            return 0, 0

        x = coord[0]
        if isinstance(x, int):
            x = x - self._offset[0]
            if x < 0 or x >= self._grid.shape[0]:
                raise IndexError("Outside of grid")
        elif isinstance(x, slice):
            x = copy(x)
            if x.start is not None:
                x.start = x.start - self._offset[0]
                if x.start < 0 or x.start >= self._grid.shape[0]:
                    raise IndexError("Outside of grid")
            if x.stop is not None:
                x.stop = x.stop - self._offset[0]
                if x.stop <= 0 or x.stop > self._grid.shape[0]:
                    raise IndexError("Outside of grid")
        else:
            raise ValueError(f"Unsupported type: {coord.__class__}")

        y = coord[1]
        if isinstance(y, int):
            y = y - self._offset[1]
            if y < 0 or y >= self._grid.shape[1]:
                raise IndexError("Outside of grid")
        elif isinstance(y, slice):
            y = copy(y)
            if y.start is not None:
                y.start = y.start - self._offset[0]
                if y.start < 0 or y.start >= self._grid.shape[1]:
                    raise IndexError("Outside of grid")
            if y.stop is not None:
                y.stop = y.stop - self._offset[0]
                if y.stop <= 0 or y.stop > self._grid.shape[1]:
                    raise IndexError("Outside of grid")
        else:
            raise ValueError(f"Unsupported type: {coord.__class__}")

        return x, y

    def deoffset_coord(self, coord: tuple[int | slice, int | slice]) -> tuple[int | slice, int | slice]:
        x = coord[0]
        if isinstance(x, int):
            x = slice(x, x)
        y = coord[1]
        if isinstance(y, int):
            y = slice(y, y)
        return slice(x.start + self._offset[0], x.stop + self._offset[0]), \
               slice(y.start + self._offset[1], y.stop + self._offset[1])

    def __getitem__(self, coord: tuple[int, int]) -> typing.Any:
        try:
            return self._grid[self.offset_coord(coord)]
        except IndexError:
            return self.fill_value

    def _fill_array(self, x: int = None, y: int = None) -> np.ndarray:
        if x is not None and y is not None:
            raise ValueError("Can only generate fill array in 1 dimension, called with both x and y parameter")
        if x is not None:
            return np.full(
                shape=(x, self._grid.shape[1]),
                dtype=self._grid.dtype,
                fill_value=self.fill_value
            )
        if y is not None:
            return np.full(
                shape=(self._grid.shape[0], y),
                dtype=self._grid.dtype,
                fill_value=self.fill_value
            )
        raise ValueError("Should specify either x or y")

    def __setitem__(self, coord: tuple[int, int], value: typing.Any) -> None:
        self._extend_grid(coord)
        self._grid[self.offset_coord(coord)] = value

    def _extend_grid(self, coord: tuple[int, int]) -> None:
        """
        Extend grid so it includes `coord`
        """
        if self._offset is None:
            self._offset = coord

        if coord[0] < self._offset[0]:  # need to extend x to the left
            dx = self._offset[0] - coord[0]
            fill_ar = self._fill_array(x=dx)
            self._grid = np.concatenate(
                (fill_ar, self._grid),
                axis=0,
            )
            self._offset = (self._offset[0] - dx, self._offset[1])
        if coord[0] >= self._offset[0] + self._grid.shape[0]:  # need to extend x to the right
            fill_ar = self._fill_array(x=coord[0] - self._offset[0] - self._grid.shape[0] + 1)
            self._grid = np.concatenate(
                (self._grid, fill_ar),
                axis=0,
            )
        if coord[1] < self._offset[1]:  # need to extend y to the top
            dy = self._offset[1] - coord[1]
            fill_ar = self._fill_array(y=dy)
            self._grid = np.concatenate(
                (fill_ar, self._grid),
                axis=1,
            )
            self._offset = (self._offset[0], self._offset[1] - dy)
        if coord[1] >= self._offset[1] + self._grid.shape[1]:  # need to extend y to the bottom
            fill_ar = self._fill_array(y=coord[1] - self._offset[1] - self._grid.shape[1] + 1)
            self._grid = np.concatenate(
                (self._grid, fill_ar),
                axis=1,
            )


if __name__ == "__main__":
    fill = 'F'
    g = InfiniteGrid(dtype='<U1', fill_value=fill)
    assert g[100, -30] == fill
    g[5, 5] = '5'
    assert g[5, 5] == '5'
    g[-6, -6] = '-'
    assert g[5, 5] == '5'
    assert g[-6, -6] == '-'
