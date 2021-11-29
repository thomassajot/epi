from heapq import heapify, heappop, heappush
from typing import List

from test_framework import generic_test


def merge_sorted_arrays(sorted_arrays: List[List[int]]) -> List[int]:
    """
        Complexity:
        >> Time: O(N*log(m)), N number of elements in all lists, m number of lists
        >> Space: O(m)
        """
    heap = [(sorted_arrays[i].pop(0), i) for i in range(len(sorted_arrays))]
    heapify(heap)
    res = []

    while len(heap) != 0:
        val, l_id = heappop(heap)
        res.append(val)
        if len(sorted_arrays[l_id]) != 0:
            heappush(heap, (sorted_arrays[l_id].pop(0), l_id))
    return res


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('sorted_arrays_merge.py',
                                       'sorted_arrays_merge.tsv',
                                       merge_sorted_arrays))
