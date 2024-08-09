import itertools 
from typing import List
""" 
Source: https://leetcode.com/problems/increasing-triplet-subsequence/
Level: LC Medium

Basic Idea:
Let idx be the mid entry
need min(arr[0]...arr[idx-1]) < arr[idx] < max(arr[idx+1]...arr[n-1])
So for each idx, let:
f(idx) = min(arr[0]...arr[idx-1])
g(idx) = max(arr[idx+1]...arr[n-1])
"""
class Solution:
    def increasing_triplet(self, nums: List[int]) -> bool:
        kLargeVal, kSmallVal = 2 ** 32, - 2 ** 32
        # f[idx] is smallest in 0...idx-1
        f = itertools.accumulate(nums, lambda x, y: min(x, y), initial=kLargeVal)
        # g[-idx-1] is largest in idx+1...n-1
        g = list(itertools.accumulate(reversed(nums), lambda x, y: max(x, y), initial=kSmallVal))
        return any(fi < ni < gi for fi, ni, gi in zip(f, nums, reversed(g)))
