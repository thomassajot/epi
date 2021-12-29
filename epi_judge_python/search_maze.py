import collections
import copy
import functools
from typing import List

from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook

WHITE, BLACK = range(2)

Coordinate = collections.namedtuple('Coordinate', ('x', 'y'))


def search_maze_perso(maze: List[List[int]], s: Coordinate,
                      e: Coordinate) -> List[Coordinate]:
    def build_graph():
        graph = collections.defaultdict(set)
        for col in range(len(maze)):
            for row in range(len(maze[0])):
                if maze[col][row] == BLACK:
                    continue
                for i, j in (1, 0), (-1, 0), (0, 1), (0, -1):
                    if 0 <= col + i < len(maze) and 0 <= row + j < len(maze[0]) and maze[col + i][row + j] != BLACK:
                        graph[Coordinate(col, row)].add(Coordinate(col + i, row + j))
        return graph

    def dfs(graph, curr, target, visited=set()):
        if curr == target:
            return [target]

        if curr in visited:
            return []

        visited.add(curr)
        for next_curr in graph[curr]:
            path = dfs(graph, next_curr, target)
            if len(path) != 0:
                break
        else:
            return []
        return [curr] + path

    return dfs(build_graph(), s, e)


def search_maze(maze: List[List[int]], s: Coordinate, e: Coordinate) -> List[Coordinate]:
    def search_dfs(curr: Coordinate):
        if not (0 <= curr.x < len(maze)
                and 0 <= curr.y < len(maze[curr.x])
                and maze[curr.x][curr.y] == WHITE):
            return False

        path.append(curr)
        maze[curr.x][curr.y] = BLACK

        if curr == e:
            return True

        if any(search_dfs(Coordinate(curr.x + x, curr.y + y)) for x, y in [(1, 0), (-1, 0), (0, 1), (0, -1)]):
            return True

        del path[-1]
        return False

    path = []
    search_dfs(s)
    return path


def path_element_is_feasible(maze, prev, cur):
    if not ((0 <= cur.x < len(maze)) and
            (0 <= cur.y < len(maze[cur.x])) and maze[cur.x][cur.y] == WHITE):
        return False
    return cur == (prev.x + 1, prev.y) or \
           cur == (prev.x - 1, prev.y) or \
           cur == (prev.x, prev.y + 1) or \
           cur == (prev.x, prev.y - 1)


@enable_executor_hook
def search_maze_wrapper(executor, maze, s, e):
    s = Coordinate(*s)
    e = Coordinate(*e)
    cp = copy.deepcopy(maze)

    path = executor.run(functools.partial(search_maze, cp, s, e))

    if not path:
        return s == e

    if path[0] != s or path[-1] != e:
        raise TestFailure('Path doesn\'t lay between start and end points')

    for i in range(1, len(path)):
        if not path_element_is_feasible(maze, path[i - 1], path[i]):
            raise TestFailure('Path contains invalid segments')

    return True


if __name__ == '__main__':
    maze = [[0, 1, 0, 1, 0], [0, 0, 0, 1, 0], [0, 1, 1, 0, 1], [1, 0, 0, 0, 0], [1, 0, 0, 1, 1], [0, 0, 0, 0, 0],
            [1, 0, 0, 1, 0], [0, 0, 0, 0, 0], [1, 0, 1, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 1, 1], [0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0], [1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 1, 0], [1, 0, 0, 1, 0], [1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [1, 1, 1, 0, 0], [0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1]]
    s = Coordinate(8, 3)
    e = Coordinate(17, 1)
    print(search_maze(maze, s, e))
    exit(
        generic_test.generic_test_main('search_maze.py', 'search_maze.tsv',
                                       search_maze_wrapper))
