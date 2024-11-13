from typing import List


"""
Given an array with not necessarily distinct integer entries, modify it in-place
to the lexicographically next permutation. If the array is already the
lexicographically largest, wrap around to the smallest.

Source: 
Level: LC Medium

Basic idea: 
Observe the general pattern of how a next permutation is formed:
[1, 2, 3, 4]
[1, 2, 4, 3]
[1, 3, 2, 4]
[1, 3, 4, 2]

Basically, we look for the longest suffix that is sorted in reverse order.
So for example, in [1, 2, 4, 3] this suffix is [4, 3]. We take the smallest
number in this suffix that is larger than the number preceding this suffix (2),
and put this number in the predecessor's place, and sort the remaining suffix.
So in this case:
-> 3 replaces the 2
-> the new suffix is sorted([4, 2]) = [2, 4]
The full permutation is [1, 3, 2, 4]
"""
class Solution:
    def next_permutation(self, nums: List[int]) -> None:
        self.n = len(nums)
        return self.solve(nums)

    def solve(self, nums: List[int]):
        # find longest tail that is non-increasing
        idx = self.n-1
        while idx and nums[idx-1] >= nums[idx]:
            idx -= 1
        # at this point, nums[idx:] is non-increasing
        if idx == 0:
            # reached last permutation; return first
            nums.reverse()
            return
        
        # identify the first number in tail that's > nums[idx-1]
        pos = next(
            i for i in range(self.n-1, idx-1, -1) if nums[i] > nums[idx-1])
        nums[idx-1], nums[pos] = nums[pos], nums[idx-1]
        nums[idx:] = sorted(nums[idx:])
        return
