from collections import Counter
from typing import List

""" 
Problem source: https://leetcode.com/problems/detect-squares/description/

Abridged problem description: 
Design a structure that supports adding points (with duplicates) and counting
the number of axis aligned squares that can be formed including a given query
point.
# Your DetectSquares object will be instantiated and called as such:
# obj = DetectSquares()
# obj.add(point)
# param_2 = obj.count(point)

Basic idea:
Store points by x-coordinate. For each xcoord, have a Counter of ycoords.

Adding a point:
- update relevant counter (O(1))

Querying a point P:
    for each point Q in same column:
        count squares can be made with P, Q

Counting squares with (P, Q) is an O(1) operation - set membership queries.
Worst case O(n) query performance, and O(nq) overall time complexity, which
is within problem requirements. 
A little care must be taken to correctly handle the requirements of counting 
duplicates and not counting zero-area squares.
"""
NUM_COORDS = 1001
class DetectSquares:
    def __init__(self):
        self.x2ys = [Counter() for _ in range(NUM_COORDS)]

    def add(self, point: List[int]) -> None:
        x, y = point
        self.x2ys[x][y] += 1

    def count(self, point: List[int]) -> int:
        result = 0
        x0, y0 = point

        # get other ycoords with same xcoord
        for y1, repeats in filter(lambda p: p[0] != y0, self.x2ys[x0].items()):
            result += repeats * self.forms_square(x0, y0, y1)
        return result

    def forms_square(self, x0, y0, y1) -> int:
        d = y1 - y0
        x1, x2 = x0 - d, x0 + d
        left_sq = self.count_points(x1, y0) * self.count_points(x1, y1)
        right_sq = self.count_points(x2, y0) * self.count_points(x2, y1)
        return left_sq + right_sq

    def count_points(self, x, y):
        return self.x2ys[x][y] if 0 <= x < NUM_COORDS else 0
