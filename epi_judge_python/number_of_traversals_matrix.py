from functools import lru_cache

import numpy as np
import pytest

from test_framework import generic_test


def number_of_ways(n: int, m: int) -> int:
    """
    Complexity:
    >> Time: O(nm)
    >> Space: O(nm)
    """

    @lru_cache(None)
    def foo(x, y):
        if x == 1 or y == 1:
            # only down or right
            return 1

        return foo(x - 1, y) + foo(x, y - 1)

    return foo(n, m)


def number_of_ways_optimised_space(n: int, m: int) -> int:
    """
    Complexity:
    >> Time: O(nm)
    >> Space: O(nm)
    """
    if n > n:
        n, m = m, n
    above = [1] * n  # initialise first row always has one path
    curr = [1] * n
    for r in range(1, m):
        for c in range(1, n):  # single col always has one path
            curr[c] = curr[c - 1] + above[c]
        above = curr

    return above[-1]


def variante_obstacle(mat: np.ndarray):
    # number of rows, number of cols
    n, m = mat.shape

    if mat[0, 0]:
        return 0

    @lru_cache(None)
    def foo(x, y):
        if mat[x, y]:
            return 0

        if x <= 0 or y <= 0:
            return 1

        return foo(x - 1, y) + foo(x, y - 1)

    return foo(n - 1, m - 1)


class Test:
    @pytest.mark.parametrize(
        "mat, res",
        [
            (np.array([[0, 0], [0, 0]], dtype=bool), 2),
            (np.array([[0, 1], [0, 0]], dtype=bool), 1),
            (np.array([[0, 1], [1, 0]], dtype=bool), 0),
            (np.array([[0, 0], [0, 1]], dtype=bool), 0),
            (np.array([[1, 0], [0, 0]], dtype=bool), 0),
            (np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=bool), 6),
            (np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=bool), 0),
            (np.array([[0, 0, 1], [0, 0, 0], [0, 0, 0]], dtype=bool), 5),
        ]
    )
    def test_obstacle(self, mat, res):
        print()
        print(mat)
        assert variante_obstacle(mat) == res


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('number_of_traversals_matrix.py',
                                       'number_of_traversals_matrix.tsv',
                                       number_of_ways_optimised_space))
