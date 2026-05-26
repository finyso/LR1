"""
Lab 4, Task 5, Variant 24
NumPy matrix operations and statistical analysis.
Developer: Finsky Pavel
Date: 01.05.2026
Version: 1.0
"""
import numpy as np

def swap_max_elements(matrix: np.ndarray) -> np.ndarray:
    """Swaps the maximum elements of the first and last columns."""
    if matrix.shape[1] < 2:
        return matrix
    col_first = matrix[:, 0]
    col_last = matrix[:, -1]

    max_idx_first = np.argmax(col_first)
    max_idx_last = np.argmax(col_last)

    matrix[max_idx_first, 0], matrix[max_idx_last, -1] = matrix[max_idx_last, -1], matrix[max_idx_first, 0]
    return matrix

def correlation_first_last(matrix: np.ndarray) -> float:
    """Calculates the correlation coefficient between the first and last columns."""
    col_first = matrix[:, 0]
    col_last = matrix[:, -1]
    corr_matrix = np.corrcoef(col_first, col_last)
    return corr_matrix[0, 1]