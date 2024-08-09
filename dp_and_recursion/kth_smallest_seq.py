import math
from typing import List

"""
Source: https://leetcode.com/problems/kth-smallest-instructions/description/
Level: LC Hard
"""

class Solution:
    def kthSmallestPath(self, destination: List[int], k: int) -> str:
        num_v, num_h = destination
        self.n = num_v + num_h
        return self.solve(num_h, num_v, k)

    def solve(self, num_h, num_v, k):
        if num_h == 0:
            return "V" * num_v
        if num_v == 0:
            return "H" * num_h

        # find number of strs starting w H
        n = num_h + num_v
        num_start_h = math.comb(n-1, num_v)

        if num_start_h >= k:  # k is 1-indexed
            return "H" + self.solve(num_h - 1, num_v, k)
        else:
            return "V" + self.solve(num_h, num_v - 1, k - num_start_h)
