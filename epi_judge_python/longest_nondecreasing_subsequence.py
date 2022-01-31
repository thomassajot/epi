from typing import List

from test_framework import generic_test
from itertools import combinations


def brute_force(A: List[int]) -> int:
    # Go over all combinations ie, all subset of a set of size n (len (A)).
    # Time complexity: O(n2^n)
    # Space complexity: O(1)
    longest = 1
    for size in range(2, len(A)):
        for comb in combinations(A, size):
            l = 0
            v = float('-inf')
            for value in comb:
                if v > value:
                    break
                v = value
                l += 1
            longest = max(l, longest)
    return longest


def tabulation(A: List[int]) -> int:
    # Time complexity: O(n^2)
    # Space complexity: O(n)
    table = [1] * len(A)
    for i in range(1, len(A)):
        table[i] = 1 + max((table[j] for j in range(i) if A[j] <= A[i]), default=0)
    return max(table)


def variante_1(A: List[int]) -> int:
    """Return the list of numbers"""
    table_sizes = [1] * len(A)
    table_distances = [0] * len(A)
    table_distances[0] = -1

    for i in range(1, len(A)):
        m = 0
        idx = -1
        for j in range(i):
            if A[j] <= A[i]:
                if table_sizes[j] > m:
                    m = table_sizes[j]
                    idx = j
        table_distances[i] = idx
        table_sizes[i] = m + 1

    largest_sequence_length = max(table_sizes)
    for i in reversed(range(len(A))):
        if table_sizes[i] == largest_sequence_length:
            break

    idx = i
    sequence = []
    while idx > -1:
        sequence.append(A[idx])
        idx = table_distances[idx]
    return max(table_sizes)

longest_nondecreasing_subsequence_length = variante_1
if __name__ == '__main__':
    exit(
        generic_test.generic_test_main(
            'longest_nondecreasing_subsequence.py',
            'longest_nondecreasing_subsequence.tsv',
            longest_nondecreasing_subsequence_length))
