from typing import List

""" 
Source: https://leetcode.com/problems/game-of-life/

Implements one iteration of Conway's game of life.
"""
class Solution:
    def game_of_life(self, board: List[List[int]]) -> None:
        """Does not return anything, modifies board in-place instead."""
        self.m = len(board)
        self.n = len(board[0])
        self.board = board
        new_board = [[self.process(r, c) for c in range(self.n)] for r in range(self.m)]
        board[:] = new_board

    def process(self, r, c) -> int:
        num = self.count_neighbors(r, c)
        return int(num == 3 or (num == 2 and self.board[r][c]))

    def count_neighbors(self, r, c) -> int:
        dirs = [-1, 0, 1]
        nbrs = [(r+d0, c+d1) for d0, d1 in itertools.product(dirs, dirs) if (
            (d0 or d1) and self.valid(r+d0, c+d1))]
        return sum(self.board[rr][cc] for rr, cc in nbrs)

    def valid(self, r, c) -> bool:
        return 0 <= r < self.m and 0 <= c < self.n