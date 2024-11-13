from typing import List

"""
Given an array, find a peak in O(log n) time.
A peak is an element strictly greater than its neighbors. You can assume no
consecutive elements in the array are equal.

Source: https://leetcode.com/problems/find-peak-elemen
Level: LC Med

Basic idea: divide and conquer.
If idx is not a peak, then either nums[0:idx] or nums[idx+1:] contains a peak.

Notice that we don't even need to handle a base case in solve() explicitly, our
setup automatically DTRT.
"""

DUMMY_VAL = -(1 << 32)
class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        self.n = len(nums)
        return self.solve(nums, 0, self.n-1)

    def solve(self, nums: List[int], start: int, end: int) -> int:
        mid_idx = start + (end - start) // 2
        mid_val = nums[mid_idx]
        left_val = nums[mid_idx-1] if mid_idx else DUMMY_VAL
        right_val = nums[mid_idx+1] if mid_idx+1 < self.n else DUMMY_VAL
        
        if left_val > mid_val:
            return self.solve(nums, start, mid_idx-1)
        elif right_val > mid_val:
            return self.solve(nums, mid_idx+1, end)
        else:
            return mid_idx
        