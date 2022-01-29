from functools import lru_cache
from typing import List

from test_framework import generic_test


def maximum_revenue_brute_force(coins: List[int]) -> int:
    # Time complexity: exponential
    # Space complexity: O(n)
    def maximum_subarray(left: int, right: int):
        if left == right:
            return coins[left]
        elif left > right:
            return 0

        # the opponents chooses the coin that will return the lest value for the player in the next turn.
        # So we choose the minimum option of the next round.
        take_left = coins[left] + min(maximum_subarray(left + 2, right),  # opponent takes left coin
                                      maximum_subarray(left + 1, right - 1))  # opponent takes right coin
        take_right = coins[right] + min(maximum_subarray(left + 1, right - 1),  # opponent takes left coin
                                        maximum_subarray(left, right - 2))  # opponent takes right coin
        return max(take_left, take_right)

    return maximum_subarray(0, len(coins) - 1)


def maximum_revenue_memoization(coins: List[int]) -> int:
    # Time complexity: O(n^2)
    # Space complexity: O(n)
    @lru_cache(None)
    def maximum_subarray(left: int, right: int):
        if left == right:
            return coins[left]
        elif left > right:
            return 0

        # the opponents chooses the coin that will return the lest value for the player in the next turn.
        # So we choose the minimum option of the next round.
        take_left = coins[left] + min(maximum_subarray(left + 2, right),  # opponent takes left coin
                                      maximum_subarray(left + 1, right - 1))  # opponent takes right coin
        take_right = coins[right] + min(maximum_subarray(left + 1, right - 1),  # opponent takes left coin
                                        maximum_subarray(left, right - 2))  # opponent takes right coin
        return max(take_left, take_right)

    return maximum_subarray(0, len(coins) - 1)


maximum_revenue = maximum_revenue_memoization
if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('picking_up_coins.py',
                                       'picking_up_coins.tsv',
                                       maximum_revenue))
