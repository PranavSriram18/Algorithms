from typing import List, Tuple 
"""
Given a grid with certain cells marked black. A block is a 2x2 square in the 
grid. Return the number of blocks containing 0, 1, 2, 3, and 4 black cells.
Grid dimensions are on the order of 10^5 each, while #black cells <= 10^4.

Level: LC Medium
Full Problem Description: https://leetcode.com/problems/number-of-black-blocks/submissions/1335554234/

Basic idea:
The black square set is very sparse in the grid, so instead of brute force
checking each block, loop through the black cells and only check blocks that
could contain this cell. There is a subtlety here in that we overcount blocks;
in fact a block with k black cells is counted exactly k times, which we can
easily fix in postprocessing.
"""
class Solution:
    def count_black_blocks(
            self, m: int, n: int, coordinates: List[List[int]]) -> List[int]:
        self.m = m
        self.n = n
        self.black_cells = {(row, col) for row, col in coordinates}
        return self.count_blocks()
    
    def count_blocks(self):
        # For each black cell, check all 4 blocks that could contain it
        totals  = [0] * 5
        for row, col in self.black_cells:
            block_starts = self.get_block_starts(row, col)
            for br, bc in block_starts:
                cells = [(br, bc), (br+1, bc), (br, bc+1), (br+1, bc+1)]
                curr_num_black = sum(1 for cell in cells if (cell in self.black_cells))
                totals[curr_num_black] += 1
        return self.postprocess(totals)
    
    def postprocess(self, totals: List[int]):
        for i in range(2, 5):
            totals[i] = totals[i] // i
        total_blocks = (self.m - 1) * (self.n - 1)
        totals[0] = total_blocks - sum(totals)
        return totals
    
    def get_block_starts(self, row: int, col: int) -> List[Tuple[int, int]]:
        """
        We call a "block start" the top-left cell of the block.
        Given a cell, get all blocks containing it, identified by block start.
        """
        result = [(row, col), (row, col-1), (row-1, col), (row-1, col-1)]
        return filter(lambda p: self.valid_block_start(p[0], p[1]), result)
    
    def valid_block_start(self, row: int, col: int) -> bool:
        return self.in_bounds(row, col) and self.in_bounds(row+1, col+1)

    def in_bounds(self, row: int, col: int):
        return (0 <= row < self.m) and (0 <= col < self.n)
