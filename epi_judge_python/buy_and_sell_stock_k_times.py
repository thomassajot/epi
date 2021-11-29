from typing import List

from test_framework import generic_test


def compute_extremum(arr: List[int]) -> List[int]:
    """
    Return extremum starting at a low value !
    Complexity: O(N) time, O(N) space
    """
    lows_highs = []
    if arr[0] < arr[1]:
        lows_highs.append(arr[0])

    for i in range(1, len(arr) - 1):
        if (arr[i + 1] > arr[i] < arr[i - 1]) or (arr[i + 1] < arr[i] > arr[i - 1]):
            lows_highs.append(arr[i])

    lows_highs.append(arr[len(arr) - 1])
    return lows_highs


# my personal solution, I don't know how to calculate the complexity
def buy_and_sell_stock_k_times_perso(prices: List[float], k: int) -> float:
    if k == 0:
        return 0

    if 2 * k >= len(prices):
        return sum(max(0, b - a) for a, b in zip(prices[:-1], prices[1:]))

    extremum = compute_extremum(prices)
    return buy_and_sell_rec(extremum, k)


def buy_and_sell_rec(extremum, k: int) -> float:
    if k <= 0 or len(extremum) <= 1:
        return 0

    s = 0
    final_sum = 0
    prev = extremum[0]
    for i, ext in enumerate(extremum[1:], 1):
        s = max(s + ext - prev, 0)

        if s == 0:
            # we do not need to buy if we make 0 profit
            next_k = k
        else:
            next_k = k - 1
        potential_gains = s + buy_and_sell_rec(extremum[i + 1:], next_k)
        final_sum = max(final_sum, potential_gains)
        prev = ext
    return final_sum


def buy_and_sell_stocks_k_times_dp(arr, k: int) -> float:
    """
    Complexity:
    >> Time: O(kn^2)
    >> Space: O(kn)
    """
    n = len(arr)
    profit = [[0 for i in range(k + 1)] for j in range(n)]
    for i in range(1, n):  # O(n)
        for j in range(1, k + 1):  # O(k)
            max_so_far = 0
            for l in range(i):  # O(n)
                max_so_far = max(max_so_far, arr[i] - arr[l] + profit[l][j - 1])
            profit[i][j] = max(profit[i - 1][j], max_so_far)

    return profit[n - 1][k]


def buy_and_sell_stocks_k_times_dp_optimised(prices, k: int) -> float:
    """
    Complexity:
    >> Time: O(kn^2)
    >> Space: O(n)  <- we do not need `k` here !
    """
    n = len(prices)

    # Initial profit for A[:i] given k = 0
    # no  profit is possible to initialise at 0
    profit = [0] * n
    next_profit = [0] * n
    for j in range(1, k + 1):  # O(k)
        for i in range(1, n):  # O(n)
            max_so_far = 0
            for l in range(i):  # O(n)
                max_so_far = max(max_so_far,
                                 prices[i] - prices[l] + profit[l])  # profit[l] is by default profit[l][j-1]
            next_profit[i] = max(next_profit[i - 1], max_so_far)
        profit = next_profit
        next_profit = [0] * len(prices)

    return profit[n - 1]


def buy_and_sell_stocks_k_times_dp_optimised2(prices, k: int) -> float:
    """
    Optimization from the one above buy_and_sell_stocks_k_times_dp_optimised
    see https://www.geeksforgeeks.org/maximum-profit-by-buying-and-selling-a-share-at-most-k-times/
    Complexity:
    >> Time: O(kn)  <- we removed on `n` !!!!!!
    >> Space: O(n)  <- we do not need `k` here !
    """
    if k == 0:
        return 0

    if 2 * k >= len(prices):
        return sum(max(0, b - a) for a, b in zip(prices[:-1], prices[1:]))

    n = len(prices)

    # Initial profit for A[:i] given k = 0
    # no  profit is possible to initialise at 0
    prev_profit = [0] * n
    next_profit = [0] * n
    for j in range(1, k + 1):  # O(k)
        prev_diff = float('-inf')
        for i in range(1, n):  # O(n)
            prev_diff = max(prev_diff, prev_profit[i - 1] - prices[i - 1])
            next_profit[i] = max(next_profit[i - 1], prices[i] + prev_diff)
        prev_profit = next_profit
        next_profit = [0] * len(prices)

    return prev_profit[n - 1]


def buy_and_sell_stocks_k_times_best(prices, k: int) -> float:
    # FROM THE BOOK , not understood !!!!!!!!!!!!!!!!!!!!!
    if k == 0:
        return 0

    if 2 * k >= len(prices):
        return sum(max(0, b - a) for a, b in zip(prices[:-1], prices[1:]))

    min_prices, max_profits = [float('inf')] * k, [0] * k

    pass


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('buy_and_sell_stock_k_times.py',
                                       'buy_and_sell_stock_k_times.tsv',
                                       buy_and_sell_stocks_k_times_dp_optimised2))
