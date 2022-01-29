import functools
from typing import List, Set

from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook


def decompose_into_dictionary_words_brute_force(domain: str, dictionary: Set[str]) -> List[str]:
    def rec(name):
        if len(name) == 0:
            return [], True

        for w in dictionary:
            if w == name[:len(w)]:
                res, success = rec(name[len(w):])
                if success:
                    return [w] + res, True

        return [], False

    return rec(domain)[0]


def decompose_into_dictionary_words_memoization(domain: str, dictionary: Set[str]) -> List[str]:
    @functools.lru_cache(None)
    def rec(name):
        if len(name) == 0:
            return [], True

        for w in dictionary:
            if w == name[:len(w)]:
                res, success = rec(name[len(w):])
                if success:
                    return [w] + res, True

        return [], False

    return rec(domain)[0]


def decompose_into_dictionary_words_tabulation(domain: str, dictionary: Set[str]) -> List[str]:
    # n = domain size, s = size of dictionary
    # Time Complexity: O()
    # Space Complexity: O(n)
    table = [0] * len(domain)
    for idx in range(len(domain)):  # O(n)
        if domain[:idx + 1] in dictionary:  # O(n) (at most)
            table[idx] = idx + 1
            continue

        for prev_idx in range(idx):  # O(n)
            if table[prev_idx] != 0 and domain[prev_idx + 1: idx + 1] in dictionary:  # O(n) (at most)
                table[idx] = idx - prev_idx
                break

    decompositions = []
    if table[-1] != 0:
        idx = len(table) - 1
        while idx >= 0:
            decompositions.append(domain[idx + 1 - table[idx]: idx + 1])
            idx -= table[idx]
    return decompositions[::-1]


decompose_into_dictionary_words = decompose_into_dictionary_words_tabulation


# =======================================================
# Variant palindromic decomposition

def is_palindrome(s):
    left, right = 0, len(s) - 1

    while left <= right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True


assert is_palindrome('kayak')
assert not is_palindrome('hello')
assert not is_palindrome('aabb')
assert is_palindrome('aba')


def min_palindromic_decomposition(s):
    # Time complexity: O(s^3)
    # Space: O(s)

    palindrome_sizes = [1] * len(s)
    min_palindrome = list(range(len(s) + 1))

    for i in range(len(s)):  # O(s)
        if is_palindrome(s[:i + 1]):  # O(s)
            print(s[:i + 1], 'is_palindrome')
            palindrome_sizes[i] = i + 1
            min_palindrome[i] = 1
            continue

        for j in range(i):  # O(s)
            if is_palindrome(s[j + 1:i + 1]): # O(s)
                print(s[j + 1:i + 1], 'is_palindrome')
                num_palindrome = min_palindrome[j] + 1
                if num_palindrome < min_palindrome[i]:
                    min_palindrome[i] = num_palindrome
                    palindrome_sizes[i] = i - j

    decompositions = []
    idx = len(palindrome_sizes) - 1
    while idx >= 0:
        decompositions.append(s[idx + 1 - palindrome_sizes[idx]:idx + 1])
        idx -= palindrome_sizes[idx]
    return decompositions[::-1]


assert min_palindromic_decomposition('0204451881') == ['020', '44', '5', '1881']
assert min_palindromic_decomposition('432101234') == ['432101234']
assert min_palindromic_decomposition('12345') == list('12345')


@enable_executor_hook
def decompose_into_dictionary_words_wrapper(executor, domain, dictionary, decomposable):
    result = executor.run(
        functools.partial(decompose_into_dictionary_words, domain, dictionary))

    if not decomposable:
        if result:
            raise TestFailure('domain is not decomposable')
        return

    if any(s not in dictionary for s in result):
        raise TestFailure('Result uses words not in dictionary')

    if ''.join(result) != domain:
        raise TestFailure('Result is not composed into domain')


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main(
            'is_string_decomposable_into_words.py',
            'is_string_decomposable_into_words.tsv',
            decompose_into_dictionary_words_wrapper))
