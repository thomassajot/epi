from functools import reduce
from typing import List

from test_framework import generic_test


def rabin_karp(t: str, s: str) -> int:
    """Return the first position of s in t"""
    if len(s) > len(t):
        return -1

    base = 26  # because 26 chars in alphabet
    t_hash = reduce(lambda h, c: h * base + ord(c), t[:len(s)], 0)
    s_hash = reduce(lambda h, c: h * base + ord(c), s[:len(s)], 0)
    power_s = base ** max(len(s) - 1, 0)

    for i in range(len(s), len(t)):
        if t_hash == s_hash and t[i - len(s): i] == s:
            return i - len(s)

        t_hash -= ord(t[i - len(s)]) * power_s
        t_hash = t_hash * base + ord(t[i])

    if t_hash == s_hash and t[-len(s):] == s:
        return len(t) - len(s)

    return -1


def _kmp_table(w: str) -> List[int]:
    """helper function to initalise the kmp table in the kmp algorithm"""
    pos, cnd = 1, 0
    table = [0] * (len(w) + 1)
    table[0] = -1

    while pos < len(w):
        if w[pos] == w[cnd]:
            table[pos] = table[cnd]
        else:
            table[pos] = cnd
            while cnd >= 0 and w[pos] != w[cnd]:
                cnd = table[cnd]
        pos += 1
        cnd += 1

    table[pos] = cnd
    return table


def kmp(s: str, t: str) -> int:
    j = k = 0
    T = _kmp_table(t)

    while j < len(t):
        if s[k] == t[j]:
            j += 1
            k += 1
            if k == len(s):
                return j - k

        else:
            k = T[k]
            if k < 0:
                j += 1
                k += 1
    return -1


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('substring_match.py',
                                       'substring_match.tsv', rabin_karp))
