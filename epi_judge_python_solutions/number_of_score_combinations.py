import sys
from functools import lru_cache
from typing import List

from test_framework import generic_test


def num_combinations_for_final_score(final_score: int,
                                     individual_play_scores: List[int]) -> int:

    # One way to reach 0.
    num_combinations_for_score = [[1] + [0] * final_score
                                  for _ in individual_play_scores]
    for i in range(len(individual_play_scores)):
        for j in range(1, final_score + 1):
            without_this_play = (num_combinations_for_score[i - 1][j]
                                 if i >= 1 else 0)
            with_this_play = (
                num_combinations_for_score[i][j - individual_play_scores[i]]
                if j >= individual_play_scores[i] else 0)
            num_combinations_for_score[i][j] = (without_this_play +
                                                with_this_play)
    return num_combinations_for_score[-1][-1]


def num_combinations_for_final_score_exp(final_score: int, individual_play_scores: List[int]) -> int:
    # Exponential time complexity,
    # O(S) space complexity, where S is the number of play scores. Because of the stack depth.
    def num_comb(V, scores):
        if V == 0:
            return 1

        if len(scores) == 0:
            return 0

        res = 0

        score = scores[0]
        for n in range(0, V // score + 1):  # number of times we can remove this score
            res += num_comb(V - n * score, scores[1:])
        return res

    return num_comb(final_score, individual_play_scores)


def num_combinations_for_final_score_memoization(final_score: int, individual_play_scores: List[int]) -> int:
    # V = final_score, S = # play scores
    # Time Complexity: O(VS)
    # O(VS) space complexity because we save all states in caches (states = V, Score_idx)
    @lru_cache(None)
    def num_comb(V, score_idx):
        if V == 0:
            return 1

        if score_idx == len(individual_play_scores):
            return 0

        res = 0

        score = individual_play_scores[score_idx]
        for n in range(0, V // score + 1):  # number of times we can remove this score
            res += num_comb(V - n * score, score_idx + 1)
        return res

    return num_comb(final_score, 0)


def num_combinations_for_final_score_tabulation(final_score: int, individual_play_scores: List[int]) -> int:
    table = [[0] * (final_score + 1) for _ in range(2)]

    for score in individual_play_scores:
        table[1][0] = 1
        for i in range(1, final_score + 1):
            combs = table[0][i]
            if i - score >= 0:
                combs += table[1][i - score]
            table[1][i] = combs
        table[0] = table[1]
        table[1] = [0] * (final_score + 1)

    return table[0][final_score]


if __name__ == '__main__':
    num_combinations_for_final_score = num_combinations_for_final_score_tabulation
    exit(
        generic_test.generic_test_main('number_of_score_combinations.py',
                                       'number_of_score_combinations.tsv',
                                       num_combinations_for_final_score))
