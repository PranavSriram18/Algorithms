from typing import List, Tuple

"""
Count the number of strictly increasing paths in a grid.
Full problem description: https://leetcode.com/problems/number-of-increasing-paths-in-a-grid/
Level: LC hard

Basic idea: Count the number of paths starting from a given cell. If we denote
this quantity by f(cell), then f(cell) = 1 + sum(f(gnb)), where "gnb" runs over
the set of neighbors of cell with a greater value. This recurrence leads to a
simple solution with memoization.
"""

MOD = 10 ** 9 + 7
class Solution:
    def countPaths(self, grid: List[List[int]]) -> int:
        self.m, self.n = len(grid), len(grid[0])
        self.grid = grid
        # (i, j) entry is number of increasing paths from (i, j)
        self.cache = [[0 for _ in range(self.n)] for _ in range(self.m)]
        self.total = 0
        for r in range(self.m):
            for c in range(self.n):
                self.visit(r, c)
        return self.total
        
    def visit(self, row, col) -> int:
        if self.cache[row][col]:
            return self.cache[row][col]

        curr = 1
        for nr, nc in self.greater_neighbors(row, col):
            curr += self.visit(nr, nc)
        self.cache[row][col] = curr
        self.total = (self.total + curr) % MOD
        return curr

    def greater_neighbors(self, row, col) -> List[Tuple[int, int]]:
        dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        return [(row + dr, col + dc) for dr, dc in dirs if self.in_bounds(
            row+dr, col+dc) and self.grid[row+dr][col+dc] > self.grid[row][col]]
        
    def in_bounds(self, nr, nc):
        return 0 <= nr < self.m and 0 <= nc < self.n