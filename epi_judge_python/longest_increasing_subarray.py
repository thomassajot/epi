import collections
from typing import List

from test_framework import generic_test

Subarray = collections.namedtuple('Subarray', ('start', 'end'))


def find_longest_increasing_subarray(A: List[int]) -> Subarray:
    """
    Complexity:
    >> Time: O(n)
    >> Space: O(1)
    """
    i, max_length = 0, 1
    result = Subarray(0, 0)

    while i < len(A) - max_length:
        # backward check
        for j in range(i + max_length, i, -1):
            if A[j - 1] >= A[j]:
                i = j
                break
        else:
            i += max_length
            while i < len(A) and A[i - 1] < A[i]:
                i, max_length = i + 1, max_length + 1
            result = Subarray(i - max_length, i - 1)
    return result





def find_longest_increasing_subarray_wrapper(A):
    result = find_longest_increasing_subarray(A)
    return result.end - result.start + 1


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main(
            'longest_increasing_subarray.py',
            'longest_increasing_subarray.tsv',
            find_longest_increasing_subarray_wrapper))
