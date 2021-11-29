from functools import lru_cache
from typing import List

from test_framework import generic_test


def is_pattern_contained_in_grid_perso(grid: List[List[int]],
                                       pattern: List[int]) -> bool:
    """
    Complexity:
    >> Time: O(rows*cols*pattern)
    >> Space: O(rows*cols + pattern) ?
    """
    n_rows, n_cols = len(grid), len(grid[0])
    stack = [((row, col), 0) for col in range(n_cols) for row in range(n_rows)]
    while len(stack) != 0:
        (r, c), depth = stack.pop()
        if grid[r][c] != pattern[depth]:
            continue

        if depth == (len(pattern) - 1):
            return True

        for i, j in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            if 0 <= r + i < n_rows and 0 <= c + j < n_cols:
                stack.append(((r + i, c + j), depth + 1))

    return False


def is_pattern_contained_in_grid(grid: List[List[int]],
                                 pattern: List[int]) -> bool:
    """
    Complexity:
    >> Time: O(cols * rows * pattern)
    >> Space: O(cols * rows * pattern)
    """
    @lru_cache
    def rec(x, y, offset):
        if len(pattern) == offset:
            return True
        if not (0 <= x < len(grid) and 0 <= y < len(grid[0])) or grid[x][y] != pattern[offset]:
            return False

        return any(rec(*next_xy, offset + 1) for next_xy in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)))

    return any(rec(i, j, 0) for i in range(len(grid)) for j in range(len(grid[0])))


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('is_string_in_matrix.py',
                                       'is_string_in_matrix.tsv',
                                       is_pattern_contained_in_grid))
