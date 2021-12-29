import functools
from collections import deque
from typing import List

import pytest

from test_framework import generic_test
from test_framework.test_utils import enable_executor_hook


class GraphVertex:
    WHITE, GRAY, BLACK = range(3)

    def __init__(self, name: str = 'GraphVertex') -> None:
        self.name = name
        self.edges: List['GraphVertex'] = []
        self.color = GraphVertex.WHITE
        self.visited = False

    def __repr__(self):
        return self.name


def is_deadlocked(graph: List[GraphVertex]) -> bool:
    def has_cycle(cur: GraphVertex) -> bool:
        if cur.color == GraphVertex.GRAY:
            return True
        cur.color = GraphVertex.GRAY
        if any(next.color != GraphVertex.BLACK and has_cycle(next) for next in cur.edges):
            return True

        cur.color = GraphVertex.BLACK
        return False

    return any(vertex.color == GraphVertex.WHITE and has_cycle(vertex) for vertex in graph)


def _are_edges_connected(start: GraphVertex, end: GraphVertex):
    """
    Complexity:
    >> Time: O(V + E)
    >> Space: O(V)
    """
    if start == end:
        return True

    start_q = deque([start])
    end_q = deque([end])
    clean_up = set()
    result = False
    while start_q and end_q:
        for q in (start_q, end_q):
            vertex = q.popleft()
            clean_up.add(vertex)
            if vertex.visited:
                continue
            vertex.visited = True
            for child in vertex.edges:
                if child in end_q:
                    result = True
                    break
                if not child.visited:
                    q.append(child)

    for vertex in clean_up:
        vertex.visited = False
    return result


def variant_single_edge_connected_perso(graph: List[GraphVertex]):
    """
    Return True if edges are weakly connected, False otherwise
    Complexity:

    >> Time: O(|V| + |E| * (|V| + |E|)) -> O[|E| * (|V| + |E|)]
    >> Space: O(|V|)
    """
    # BFS on all vertices
    q = deque(graph)

    while q:
        parent = q.popleft()
        if parent.color == GraphVertex.BLACK:
            continue

        parent_edges = set(parent.edges)
        for child in parent_edges:
            if child.color == GraphVertex.BLACK:
                continue
            child_edges = set(child.edges)
            parent.edges = parent_edges - {child}
            child.edges = child_edges - {parent}
            if not _are_edges_connected(parent, child):
                return True
            child.edges = child_edges
        parent.edges = parent_edges
        parent.color = GraphVertex.BLACK
    return False


def variant_single_edge_connected_bridge(graph: List[GraphVertex]):
    """
    Return True if edges are weakly connected, False otherwise
    An edge is a bridge if when removed produces more connected components.
    Which also means, that there are no cycles that include this edge !!!!
    So this is about checking cycles.

    Complexity:
    >> Time: O(|V| + |E|)
    >> Space: O(|V|)
    """

    def has_cycle(cur: GraphVertex) -> bool:
        if cur.color == GraphVertex.GRAY:
            return False
        cur.color = GraphVertex.GRAY
        if any(next.color != GraphVertex.BLACK and has_cycle(next) for next in cur.edges):
            return False

        cur.color = GraphVertex.BLACK
        return True

    return any(vertex.color == GraphVertex.WHITE and has_cycle(vertex) for vertex in graph)


@enable_executor_hook
def is_deadlocked_wrapper(executor, num_nodes, edges):
    if num_nodes <= 0:
        raise RuntimeError('Invalid num_nodes value')
    graph = [GraphVertex() for _ in range(num_nodes)]

    for (fr, to) in edges:
        if fr < 0 or fr >= num_nodes or to < 0 or to >= num_nodes:
            raise RuntimeError('Invalid vertex index')
        graph[fr].edges.append(graph[to])

    return executor.run(functools.partial(is_deadlocked, graph))


class TestVariant:
    @pytest.fixture
    def graph_1(self):
        a, b = [GraphVertex(name) for name in list('ab')]
        a.edges = [b]
        b.edges = [a]
        return [a, b]

    @pytest.fixture
    def graph_2(self):
        graph = [GraphVertex(name) for name in list('abcd')]
        a, b, c, d = graph
        a.edges = [b, c]
        b.edges = [a, d]
        c.edges = [a, d]
        d.edges = [b, c]
        return graph

    @pytest.fixture
    def graph_3(self):
        graph = [GraphVertex(name) for name in list('abcde')]
        a, b, c, d, e = graph
        a.edges = [b, c]
        b.edges = [a, d]
        c.edges = [a, d, e]
        d.edges = [b, c]
        e.edges = [c]
        return graph

    @pytest.mark.parametrize('graph, start, end',
                             [('graph_1', 0, 0), ('graph_1', 0, 1), ('graph_2', 0, 3), ('graph_3', 0, 4)])
    def test_connected(self, graph, start, end, request):
        graph = request.getfixturevalue(graph)
        assert _are_edges_connected(graph[start], graph[end])

    def test_disconnected(self, graph_1, graph_2):
        assert not _are_edges_connected(graph_1[0], graph_2[0])

    @pytest.mark.parametrize('graph, is_weakly_connected',
                             [('graph_1', True), ('graph_2', False), ('graph_3', True)])
    def test(self, graph, is_weakly_connected, request):
        graph = request.getfixturevalue(graph)
        assert variant_single_edge_connected_perso(graph) == is_weakly_connected
        assert variant_single_edge_connected_bridge(graph) == is_weakly_connected


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('deadlock_detection.py',
                                       'deadlock_detection.tsv',
                                       is_deadlocked_wrapper))
