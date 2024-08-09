from collections import Counter 
from typing import List

"""
Source: https://leetcode.com/problems/count-the-number-of-good-partitions/description/
Level: LC Hard

Problem description:
A partition of an array into one or more contiguous subarrays is called good if
no two subarrays contain the same number. Return the number of good partitions
of a given array, modulo 10**9+7.

Basic idea:
At each of (n-1) positions, either place a divider or don't
So just count number of valid positions to place a divider
Use running sets (Counter) to keep track of what numbers appear to the left and
right of a given pos
"""
MOD = 10 ** 9 + 7
class Solution:
    def numberOfGoodPartitions(self, nums: List[int]) -> int:
        self.nums = nums
        self.n = len(nums)
        return pow(2, self.num_dividers(), MOD)

    def num_dividers(self):
        total = 0
        empty = Counter()
        left = Counter()
        right = Counter(self.nums)
        inters = set()  # dynamically maintain left & right
        for num in self.nums[0:-1]:
            left[num] += 1
            right[num] -= 1
            if not right[num]:
                inters.discard(num)
            else:
                inters.add(num)
            if not inters:
                total += 1
        return total
