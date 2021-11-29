from functools import lru_cache

from test_framework import generic_test


def compute_binomial_coefficient_perso(n: int, k: int) -> int:
    @lru_cache(None)
    def foo(i, j):
        if j == 0:
            return 1

        if j > i:
            return 0

        if i == j:
            return 1

        if j == 1:
            return i

        return foo(i - 1, j) + foo(i - 1, j - 1)
    return foo(n, k)


@lru_cache(None)
def compute_binomial_coefficient(n: int, k: int) -> int:
    """
    Complexity:
    >> Time: O(nk)
    >> Space: O(nk)
    """
    if k in (0, n):
        return 1

    return compute_binomial_coefficient(n - 1, k) + compute_binomial_coefficient(n - 1, k - 1)



if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('binomial_coefficients.py',
                                       'binomial_coefficients.tsv',
                                       compute_binomial_coefficient))
