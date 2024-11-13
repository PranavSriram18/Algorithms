
import bisect
import itertools
import random
from typing import List

"""
Implement sampling from a weighted distribution over {0, ..., k-1} with
weights given by an array w.
Full problem description: https://leetcode.com/problems/random-pick-with-weight/description
Level: LC Med

Basic idea: Prefix sum + bisection
"""
class Solution:

    def __init__(self, w: List[int]):
        self.n = len(w)
        self.pfx = list(itertools.accumulate(w))
        self.S = self.pfx[-1]

    def pickIndex(self) -> int:
        k = random.randint(1, self.S)
        idx = bisect.bisect_left(self.pfx, k)
        return idx