from collections import defaultdict
from functools import lru_cache
from typing import List

from test_framework import generic_test


def num_combinations_for_final_score(final_score: int,
                                     individual_play_scores: List[int]) -> int:
    """
    Complexity: s = final_score, n = number of individual scores
    >> Time: O(sn)
    >> Space: O(sn)
    """
    num_combinations_for_score = [[1] + [0] * final_score for _ in individual_play_scores]

    for i in range(len(individual_play_scores)):
        for j in range(1, final_score + 1):
            without_this_play = num_combinations_for_score[i - 1][j] if i >= 1 else 0
            if j >= individual_play_scores[i]:
                with_this_play = num_combinations_for_score[i][j - individual_play_scores[i]]
            else:
                with_this_play = 0
            num_combinations_for_score[i][j] = without_this_play + with_this_play
    return num_combinations_for_score[-1][-1]


def variant_num_combinations_for_final_score_better_space(final_score: int, individual_play_scores: List[int]) -> int:
    """
    Complexity: s = final_score, n = number of individual scores
    >> Time: O(sn)
    >> Space: O(s) !!!!!!!!!!! We use only 2s space by overwriting the prev-prev-row
    """

    num_combinations_for_score = [[1] + [0] * final_score for _ in range(2)]
    curr_row = 0
    prev_row = -1
    for i in range(len(individual_play_scores)):
        curr_row = (curr_row + 1) % 2
        prev_row = (prev_row + 1) % 2

        for j in range(1, final_score + 1):
            without_this_play = num_combinations_for_score[prev_row][j]
            if j >= individual_play_scores[i]:
                with_this_play = num_combinations_for_score[curr_row][j - individual_play_scores[i]]
            else:
                with_this_play = 0
            num_combinations_for_score[curr_row][j] = without_this_play + with_this_play

    return num_combinations_for_score[curr_row][-1]


def variant_num_sequences_for_final_score_brute_force_rec(final_score: int, individual_play_scores: List[int]) -> int:
    plays = set(individual_play_scores)
    comb = 0

    def rec(score):
        nonlocal comb
        if score in plays:
            # True is the end
            comb += 1

        if score <= 0:
            return

        for value in individual_play_scores:
            rec(score - value)

    rec(final_score)
    return comb


def variant_num_sequences_for_final_score_rec_cached(final_score: int, individual_play_scores: List[int]) -> int:
    plays = set(individual_play_scores)

    @lru_cache()
    def rec(score):
        comb = 0
        if score <= 0:
            return comb

        if score in plays:
            comb += 1

        for value in individual_play_scores:
            comb += rec(score - value)
        return comb

    return rec(final_score)


def variant_num_sequences_for_final_score_bottom_up(final_score: int, individual_play_scores: List[int]) -> int:
    """
    Complexity:
    >> Time: O(sn)
    >> Space: O(s)
    """
    comb = defaultdict(int)
    for score in range(1, final_score + 1):
        if score in individual_play_scores:
            comb[score] += 1

        for single_score in individual_play_scores:
            comb[score] += comb[score - single_score]

    return comb[final_score]


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('number_of_score_combinations.py',
                                       'number_of_score_combinations.tsv',
                                       num_combinations_for_final_score))
