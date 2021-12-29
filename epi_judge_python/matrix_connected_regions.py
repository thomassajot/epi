from collections import deque
from typing import List

from test_framework import generic_test


def flip_color_perso(x: int, y: int, image: List[List[bool]]) -> None:
    """
    Complexity:
    >> Time: O(V)
    >> Space: O(V)
    """
    color: bool = image[x][y]

    def search(r, c):
        if not (0 <= r < len(image) and 0 <= c < len(image[0]) and image[r][c] == color):
            return False

        image[r][c] = not color
        for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            search(r + i, c + j)

    search(x, y)


def flip_color(x: int, y: int, image: List[List[bool]]) -> None:
    color: bool = image[x][y]
    queue = deque([(x, y)])
    while len(queue) > 0:
        r, c = queue.popleft()

        image[r][c] = not color
        for i, j in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
            if 0 <= i < len(image) and 0 <= j < len(image[0]) and image[i][j] == color:
                queue.append((i, j))


def flip_color_wrapper(x, y, image):
    flip_color(x, y, image)
    return image


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('matrix_connected_regions.py',
                                       'painting.tsv', flip_color_wrapper))
