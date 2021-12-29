from typing import List

from test_framework import generic_test


def calculate_largest_rectangle_brute_force(heights: List[int]) -> int:
    """
    Complexity:
    >> Time: O(n^2)
    >> Space: O(1)
    """
    max_area = 0

    for i, h in enumerate(heights):
        l, r = i, i

        while l - 1 >= 0 and heights[l - 1] >= h:
            l -= 1
        while r + 1 < len(heights) and heights[r + 1] >= h:
            r += 1

        area = h * (r - l + 1)
        # print(h, i, '|', r, l, area)
        max_area = max(max_area, area)
    return max_area


def calculate_largest_rectangle(heights: List[int]) -> int:
    """
    Complexity:
    >> Time: O(n)
    >> Space: O(n)
    """
    pillar_indices = []
    max_area = 0
    for i, h in enumerate(heights + [0]):
        while pillar_indices and heights[pillar_indices[-1]] >= h:
            height = heights[pillar_indices.pop()]
            width = i if not pillar_indices else i - pillar_indices[-1] - 1
            max_area = max(max_area, height * width)
        pillar_indices.append(i)
    return max_area


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('largest_rectangle_under_skyline.py',
                                       'largest_rectangle_under_skyline.tsv',
                                       calculate_largest_rectangle))
