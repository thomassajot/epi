from functools import lru_cache

from test_framework import generic_test


def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    v0 = 0
    v1 = 1
    for i in range(2, n + 1):
        v1, v0 = v0 + v1, v1
    return v1

if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('fibonacci.py', 'fibonacci.tsv',
                                       fibonacci))
