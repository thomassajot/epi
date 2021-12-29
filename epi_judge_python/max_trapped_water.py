from typing import List

from test_framework import generic_test


def get_max_trapped_water_brute_force(heights: List[int]) -> int:
    """
    Complexity:
    >> Time: O(n^2)
    >> Space: O(1)
    """
    area = -1
    for i in range(len(heights)):
        for j in range(i + 1, len(heights)):
            area = max(area, min(heights[i], heights[j]) * (j - i))
    return area


def get_max_trapped_water(heights: List[int]) -> int:
    """
    Complexity:
    >> Time: O(n)
    >> Space: O(1)
    """
    left, right = 0, len(heights) - 1
    area = -1
    while left < right:
        area = max(area, min(heights[left], heights[right]) * (right - left))
        if heights[right] <= heights[left]:
            right -= 1
        else:
            left += 1
    return area


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('max_trapped_water.py',
                                       'max_trapped_water.tsv',
                                       get_max_trapped_water))
