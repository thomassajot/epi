from functools import lru_cache

from test_framework import generic_test


def number_of_ways_to_top(top: int, maximum_step: int) -> int:
    # k = number of steps, n = top
    # Time complexity: O(KN)
    # Space: O(N)
    @lru_cache(None)
    def calculate(i):
        if i <= 1:
            return 1
        return sum(calculate(i - step) for step in range(1, min(i, maximum_step) + 1))
    return calculate(top)


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('number_of_traversals_staircase.py',
                                       'number_of_traversals_staircase.tsv',
                                       number_of_ways_to_top))
