import sys
from functools import lru_cache
from typing import List

from test_framework import generic_test


def minimum_path_weight_brute_force(triangle: List[List[int]]) -> int:
    # n is depth of triangle
    # Time complexity: O(2^n)
    # Space complexity: O(n)

    if len(triangle) == 0:
        return 0

    def rec(lvl, pos):
        if lvl == -1:
            return 0

        if pos < 0 or pos > lvl:
            return float('inf')

        return triangle[lvl][pos] + min(rec(lvl - 1, pos - 1), rec(lvl - 1, pos))

    return min(rec(len(triangle) - 1, i) for i in range(len(triangle)))


def minimum_path_weight_memoization(triangle: List[List[int]]) -> int:
    # n is depth of triangle
    # Time complexity: O(n^2)
    # Space complexity: O(n^2)

    if len(triangle) == 0:
        return 0

    @lru_cache(None)
    def rec(lvl, pos):
        if lvl == -1:
            return 0

        if pos < 0 or pos > lvl:
            return float('inf')

        return triangle[lvl][pos] + min(rec(lvl - 1, pos - 1), rec(lvl - 1, pos))

    return min(rec(len(triangle) - 1, i) for i in range(len(triangle)))


def minimum_path_weight_tabulation(triangle: List[List[int]]) -> int:
    # n is depth of triangle
    # W[n][pos] = T[n][pos] + min(T[n - 1][pos - 1], T[n - 1][pos])
    # Time complexity: O(n^2)
    # Space complexity: O(n)
    if len(triangle) == 0:
        return 0

    # initialise with first element of triangle
    prev = [triangle[0][0]]
    for level in range(1, len(triangle)):
        curr = [0] * (level + 1)
        for pos in range(len(curr)):
            left_parent = prev[pos - 1] if pos - 1 >= 0 else float('inf')
            right_parent = prev[pos] if pos < level else float('inf')
            curr[pos] = triangle[level][pos] + min(left_parent, right_parent)
        prev = curr
    return min(prev)


minimum_path_weight = minimum_path_weight_tabulation
if __name__ == '__main__':
    exit(
        generic_test.generic_test_main(
            'minimum_weight_path_in_a_triangle.py',
            'minimum_weight_path_in_a_triangle.tsv', minimum_path_weight))
