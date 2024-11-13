from typing import List

"""
Given a list of 1s and 0s, you are allowed to flip up to k 0s to 1s.

Return the largest number of consecutive 1s you can produce. 

Source: https://leetcode.com/problems/max-consecutive-ones-iii/description
Level: LC Med

Basic idea: 
Equivalently, want longest interval containing at most k zeroes.

Use two pointers: left, right represent endpoints of current interval (incl).
"""

class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        n = len(nums)
        left, right, best, num_zeros = 0, -1, 0, 0

        while True:
            while num_zeros <= k and right < n-1:
                right += 1
                num_zeros += int(nums[right] == 0)
            # either overshot or reached end
            if num_zeros > k:  # overshot
                best = max(best, right-left)
                while num_zeros > k:
                    num_zeros -= int(nums[left] == 0)
                    left += 1
            else:  # reached end
                best = max(best, right-left+1)
                return best