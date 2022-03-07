"""
Question:
    You are given a makefile
    A Makefile as a list of target. Each target can have 0, 1 or multiple dependencies (other target)
    Write an algorithm that will build the target given by the user

Answer:

    1. We can represent the dependencies as a dictionary,
    where the key is the target and the value is a list of other targets

    The Makefile with targets A, B, C, D would be: dict(A=[], B=[A], C=[B, D], D=[])
    A - B - C
           /
    D ----


    2. We can see that if we have a many more targts than what is required to build the desired target, we need to filter them out.

    Given the following makefile: dict(A=[], B=[A], C=[B, D], D=[], E=[], W = [E])
        - to build W we only need the subgraph: dict(E=[], W = [E])
        - to build C we only need to subgraph: dict(A=[], B=[A], C=[B, D], D=[])

    A - B - C     E - W
           /
    D ----

    3. Once we have the subgraph, we need to return a list of the target in the right order
    For the subgraph: dict(A=[], B=[A], C=[B, D], D=[]), the result is [A, D, B, C] (or [A, B, D, C], or [D, A, B, C])

    This is a topological sort !

Questions:
    - Do we have cycles ?
"""
from collections import defaultdict
from typing import Dict, List, Tuple

Graph = Dict[str, List[str]]


def _extract_sub_graph(target: str, graph: Graph) -> Tuple[Graph, Dict[str, int]]:
    sub_graph = defaultdict(list)
    sub_graph_counts = defaultdict(int)
    queue = [target]
    visited = set()
    # Time complexity: O(N + K)
    # Space complexity: O(N + K)
    while queue:
        t = queue.pop()
        deps = graph[t]
        sub_graph_counts[t] = len(deps)

        if t not in visited:
            queue.extend(deps)
            for d in deps:
                sub_graph[d].append(t)
            visited.add(t)
    return sub_graph, sub_graph_counts


def _build_execution_sequence(sub_graph, sub_graph_counts) -> List[str]:
    # Build execution sequence from sub-graph
    # Time complexity: O(N + K)
    # Space complexity: O(N + K)
    queue = [t for t, n_deps in sub_graph_counts.items() if n_deps == 0]
    execution = []
    while queue:
        t = queue.pop()

        execution.append(t)
        for child in sub_graph[t]:
            sub_graph_counts[child] -= 1
            if sub_graph_counts[child] == 0:
                queue.append(child)
    return execution


def build_execution_sequence(target: str, graph: Graph) -> List[str]:
    # get the subgraph, we can do counts !!!!!!!!!!! instead of listing the dependencies.
    sub_graph, sub_graph_counts = _extract_sub_graph(target, graph)
    return _build_execution_sequence(sub_graph, sub_graph_counts)


if __name__ == '__main__':
    graph = dict(a=[], b=['a'], d=[], e=[], w=['e'], c=['b', 'd'])

    assert build_execution_sequence('a', graph) == ['a']
    assert build_execution_sequence('b', graph) == ['a', 'b']
    assert build_execution_sequence('c', graph) == ['a', 'b', 'd', 'c']
    assert build_execution_sequence('e', graph) == ['e']
    assert build_execution_sequence('w', graph) == ['e', 'w']

    # graph with cycle
    # a -> b -> d -> c
    #  and d -> b
    graph = dict(a=[], b=['a', 'd'], d=['b'], e=[], w=['e'], c=['b', 'd'])

    assert build_execution_sequence('a', graph) == ['a']
    # undefined result, maybe we should return an empty list !
    assert build_execution_sequence('b', graph) == ['a']
