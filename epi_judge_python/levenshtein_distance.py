import copy
from functools import lru_cache

from test_framework import generic_test


def levenshtein_distance(A: str, B: str) -> int:
    """
    Complexity:
    >> Time: O(ab)
    >> Space: O(ab)
    """

    @lru_cache(None)
    def compute_distance_between_prefixes(A_idx, B_idx):
        if A_idx < 0:
            return B_idx + 1
        if B_idx < 0:
            return A_idx + 1

        if A[A_idx] == B[B_idx]:
            return compute_distance_between_prefixes(A_idx - 1, B_idx - 1)

        substitute_last = compute_distance_between_prefixes(A_idx - 1, B_idx - 1)
        add_last = compute_distance_between_prefixes(A_idx - 1, B_idx)
        delete_last = compute_distance_between_prefixes(A_idx, B_idx - 1)
        return 1 + min(substitute_last, add_last, delete_last)

    return compute_distance_between_prefixes(len(A) - 1, len(B) - 1)


def variant_levenshtein_distance_less_space(A: str, B: str) -> int:
    """
    Complexity:
    >> Time: O(ab)
    >> Space: O(min(a, b))
    """
    if len(A) > len(B):
        # A is the smaller string
        A, B = B, A

    la, lb = len(A), len(B)
    cache_prev = list(range(la + 1))
    cache_cur = [0] + [0] * la

    for B_idx in range(lb):
        cache_cur[0] = B_idx + 1
        for A_idx in range(1, la + 1):
            if B[B_idx] == A[A_idx - 1]:
                cache_cur[A_idx] = cache_prev[A_idx - 1]
            else:
                cache_cur[A_idx] = 1 + min(cache_prev[A_idx], cache_cur[A_idx - 1], cache_prev[A_idx - 1])
        cache_prev = copy.copy(cache_cur)

    return cache_prev[-1]


def variant_longest_common_subsequence(A: str, B: str) -> int:
    @lru_cache(None)
    def longest_common_subsequence_between_prefixes(A_idx, B_idx):
        if min(B_idx, A_idx) < 0:
            return []

        if A[A_idx] == B[B_idx]:
            return [A[A_idx]] + longest_common_subsequence_between_prefixes(A_idx - 1, B_idx - 1)

        delete_from_A = longest_common_subsequence_between_prefixes(A_idx - 1, B_idx)
        delete_from_B = longest_common_subsequence_between_prefixes(A_idx, B_idx - 1)
        return delete_from_A if len(delete_from_A) >= len(delete_from_B) else delete_from_B

    return longest_common_subsequence_between_prefixes(len(A) - 1, len(B) - 1)


@lru_cache(None)
def is_palindrome(s: str) -> True:
    left, right = 0, len(s) - 1
    while left < right:
        left += 1
        right -= 1

        if s[left] != s[right]:
            return False

    return s[left] == s[right]


@lru_cache(None)
def variant_distance_to_palindrome(A: str) -> int:
    if is_palindrome(A):
        return 0

    dist = len(A) - 1
    for i in range(len(A)):
        dist = min(dist, variant_distance_to_palindrome(A[:i] + A[i + 1:]))
    return dist + 1


def variant_distance_to_regex(A: str, r: str) -> int:
    # TODO
    # TOO HARD !!!!!!!!!!!
    return 0


def variant_is_interleaving(s1, s2, t) -> bool:
    # TODO
    return False


if __name__ == '__main__':
    print(variant_longest_common_subsequence('Carthorse', 'Orchestra'))
    print(variant_distance_to_palindrome('Carthorse'))
    print(variant_distance_to_palindrome('kayaka'))
    print('=' * 40)
    print('=' * 40)
    exit(
        generic_test.generic_test_main('levenshtein_distance.py',
                                       'levenshtein_distance.tsv',
                                       variant_levenshtein_distance_less_space))
