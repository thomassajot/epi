import collections
import functools
from typing import List, Tuple

from test_framework import generic_test
from test_framework.test_utils import enable_executor_hook
from heapq import heappop, heapify, heappush

Item = collections.namedtuple('Item', ('weight', 'value'))

Node = collections.namedtuple('Node', ('items_left', 'value', 'capacity'))


class Node(collections.namedtuple('Node', ('items_left', 'value', 'capacity'))):
    __slots__ = ()

    def __repr__(self):
        return f'Node(items_left={len(self.items_left)}, value={self.value}, capacity={self.capacity})'


def optimum_subject_to_capacity_perso(items: List[Item], capacity: int) -> int:
    item_ids = set(list(range(len(items))))

    @functools.lru_cache(None)
    def foo(items_so_far, capacity_left: int):
        if capacity_left <= 0:
            return 0

        remaining_items = item_ids - set(items_so_far)

        return max(items[i].value + foo(tuple(sorted(items_so_far + (i,))), capacity_left - items[i].weight) for i in
                   remaining_items)

    return foo(tuple(), capacity)


def optimum_subject_to_capacity_branch_and_bound_not_working(items: List[Item], capacity: int) -> int:
    # sort items by their best value to weight ratio
    items = sorted(items, key=lambda x: x.value / x.weight)
    items_vw_ratio = [x.value / x.weight for x in items]

    def heuristic(node: Node):
        # given the remaining capacity, what is the expected value l
        try:
            best_vw = max(items_vw_ratio[i] for i in node.items_left if items[i].weight <= node.capacity)
        except:
            best_vw = 0
        return - (best_vw * node.capacity + node.value)

    start_node = Node(items_left=set(list(range(len(items)))), value=0, capacity=capacity)
    heap = [(heuristic(start_node), start_node)]

    max_so_far = 0
    c = 0
    while len(heap) != 0:
        c += 1
        (expected_value, node) = heap.pop()
        max_so_far = max(node.value, max_so_far)

        if - expected_value <= max_so_far:
            continue

        if node.capacity == 0:
            continue

        for i in node.items_left:
            item = items[i]
            if item.weight <= node.capacity:
                new_node = Node(items_left=node.items_left - set([i]), value=node.value + item.value,
                                capacity=node.capacity - item.weight)
                expected_value = heuristic(new_node)
                heappush(heap, (expected_value, new_node))

    return max_so_far


def optimum_subject_to_capacity(items: List[Item], capacity: int) -> int:
    @functools.lru_cache(None)
    def build_backpack(k, available_capacity):
        if k < 0:
            return 0

        with_item = 0
        item = items[k]
        if item.weight <= available_capacity:
            with_item = item.value + build_backpack(k - 1, available_capacity=available_capacity - item.weight)
        without_item = build_backpack(k - 1, available_capacity=available_capacity)
        return max(without_item, with_item)

    return build_backpack(len(items) - 1, capacity)


def optimum_subject_to_capacity_reduced_space(items: List[Item], capacity: int) -> int:
    @functools.lru_cache(None)
    def build_backpack(k, available_capacity):
        if k < 0:
            return 0

        with_item = 0
        item = items[k]
        if item.weight <= available_capacity:
            with_item = item.value + build_backpack(k - 1, available_capacity=available_capacity - item.weight)
        without_item = build_backpack(k - 1, available_capacity=available_capacity)
        return max(without_item, with_item)

    return build_backpack(len(items) - 1, capacity)


@enable_executor_hook
def optimum_subject_to_capacity_wrapper(executor, items, capacity):
    items = [Item(*i) for i in items]
    return executor.run(
        functools.partial(optimum_subject_to_capacity, items, capacity))


def divide_the_spoils_fairly(items):
    total_value = sum(item.value for item in items)

    @functools.lru_cache(None)
    def separate(k, remaining_value) -> Tuple[List[int], int]:
        if k < 0:
            return [], remaining_value

        item = items[k]
        without_item, without_item_remaining_value = separate(k - 1, remaining_value)
        if remaining_value - item.value >= 0:
            with_item, with_item_remaining_value = separate(k-1, remaining_value - item.value)

            if with_item_remaining_value >= without_item_remaining_value:
                return with_item + [k], with_item_remaining_value

        return without_item, without_item_remaining_value

    return separate(len(items) - 1, total_value // 2)


def divide_the_spoils_fairly_and_equally(items):
    """TODO Too hard"""
    return 0


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('knapsack.py', 'knapsack.tsv',
                                       optimum_subject_to_capacity_wrapper))
