from collections import deque
from typing import List

"""
Problem source: https://leetcode.com/problems/coloring-a-border/description/
Level: LC Medium

Solution idea: Straightforward; just run a BFS starting from the start cell. 
Enqueue cells with the same color, track seen cells, and mark cells with under
4 neighbors w the same color as being part of the border.
"""
class Solution:
    def color_border(self, grid: List[List[int]], row: int, col: int, color: int) -> List[List[int]]:
        self.grid = grid
        self.m = len(grid)  # num rows
        self.n = len(grid[0])  # num cols
        border = self.run_bfs(row, col)
        for i, j in border:
            self.grid[i][j] = color
        return self.grid

    def run_bfs(self, row: int, col: int) -> List[tuple[int, int]]:
        border = []
        comp_color = self.grid[row][col]
        q = deque([(row, col)])
        seen = [[False] * self.n for _ in range(self.m)]
        seen[row][col] = True
        while len(q):
            curr_row, curr_col = q.popleft()
            neighbors = self.get_neighbors(curr_row, curr_col)
            for nr, nc in neighbors:
                if self.grid[nr][nc] == comp_color and not seen[nr][nc]:
                    seen[nr][nc] = True
                    q.append((nr, nc))
            num_colored_neighbors = num_colored_neighbors = sum(1 for x in neighbors if self.grid[x[0]][x[1]] == comp_color)
            if (num_colored_neighbors < 4):
                border.append((curr_row, curr_col))
        return border 

    def get_neighbors(self, row: int, col: int) -> List[tuple[int, int]]:
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.m and 0 <= nc < self.n:
                neighbors.append((nr, nc))
        return neighbors
    