from functools import lru_cache
from typing import List

from test_framework import generic_test

def cal_messiness(width, max_width) -> int:
    return (width - max_width) ** 2

def minimum_messiness_brute_force(words: List[str], line_length: int) -> int:
    # time complexity: O(l^n)
    # Space complexity: O(n)
    def minimum_messiness_at_word(w_idx: int) -> int:
        if w_idx >= len(words):
            return 0

        line_width = -1
        min_messiness = float('inf')

        # take some words in a line
        for i in range(w_idx, len(words)):
            line_width += 1 + len(words[i])
            if line_width > line_length:
                break
            messiness = cal_messiness(line_length, line_width)
            next_line_messiness = minimum_messiness_at_word(i + 1)
            min_messiness = min(min_messiness, messiness + next_line_messiness)
        return min_messiness

    return minimum_messiness_at_word(0)


def minimum_messiness_memoization(words: List[str], line_length: int) -> int:
    # time complexity: O(ln)
    # Space complexity: O(ln)
    @lru_cache(None)
    def minimum_messiness_at_word(w_idx: int) -> int:
        if w_idx >= len(words):
            return 0

        line_width = -1
        min_messiness = float('inf')

        # take some words in a line
        for i in range(w_idx, len(words)):
            line_width += 1 + len(words[i])
            if line_width > line_length:
                break
            messiness = cal_messiness(line_length, line_width)
            next_line_messiness = minimum_messiness_at_word(i + 1)
            min_messiness = min(min_messiness, messiness + next_line_messiness)
        return min_messiness

    return minimum_messiness_at_word(0)


def minimum_messiness_tabulation(words: List[str], line_length: int) -> int:

    # initialise first messiness
    messiness_table = [(len(words[0]) - line_length) ** 2] + [float('inf')] * (len(words) - 1)

    for i in range(1, len(words)):
        line_width = -1
        for j in reversed(range(i + 1)):
            line_width += len(words[j]) + 1  # plus white space
            if line_width > line_length:
                break
            line_messiness = cal_messiness(line_width, line_length)
            previous_line_messiness = messiness_table[j - 1] if j > 0 else 0
            messiness_table[i] = min(line_messiness + previous_line_messiness, messiness_table[i])
    return messiness_table[-1]


minimum_messiness = minimum_messiness_tabulation

if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('pretty_printing.py',
                                       'pretty_printing.tsv',
                                       minimum_messiness))
