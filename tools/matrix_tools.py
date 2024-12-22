from fractions import Fraction

import numpy as np


def matrix_minor(m: np.array, row: int, col: int) -> np.array:
    """
    Returns the matrix `m` with row `row` and column `col` removed
    """
    without_row = m[
                  [_ for _ in range(m.shape[0]) if _ != row],
                  :,
                  ]
    without_row_and_col = without_row[
                          :,
                          [_ for _ in range(m.shape[1]) if _ != col],
                          ]
    return without_row_and_col


def matrix_determinant(m: np.ndarray) -> Fraction | int:
    """
    Returns the determinant of the given matrix.
    Similar to numpy.linalg.det(), but keeps integers instead of going to float
    """
    if m.shape[0] != m.shape[1]:
        raise ValueError(f"Expected square matrix, got {m.shape}")
    N = m.shape[0]
    if N == 1:
        return int(m[0, 0])
    det = 0
    for i in range(N):
        minor = matrix_minor(m, 0, i)
        det_minor = matrix_determinant(minor)
        det += (-1)**i * int(m[0, i]) * det_minor
    return det


def matrix_inverse(m: np.ndarray) -> np.ndarray:
    """
    Does numpy.inverse(m), but returns Fractions instead of floats
    """
    det = matrix_determinant(m)
    inv = np.empty(m.shape, dtype='object')
    for _ in (it := np.nditer(m, flags=['multi_index'])):
        row, col = it.multi_index
        inv[row, col] = (-1)**(row + col) * Fraction(matrix_determinant(matrix_minor(m, row, col)), det)
    inv = inv.transpose()
    return inv


if __name__ == "__main__":
    A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    assert matrix_determinant(A) == 0

    A = np.array([[1, 2], [3, 4]])
    assert matrix_determinant(A) == -2
    B = matrix_inverse(A)
    assert np.all(np.matmul(A, B) == np.eye(2))
    assert np.all(np.matmul(B, A) == np.eye(2))
