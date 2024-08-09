from typing import List, Tuple 

""" 
Given an integer array nums, return the maximum result of nums[i] XOR nums[j], 
where 0 <= i <= j < n.

Problem Source: https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/description/
Level: LC Medium

Basic idea:
The idea is to greedily solve for each bit.
Partition the list of nums based on the msb; suppose this is the kth bit.
If both sublists are nonempty, the solution *must* contain one number from each
sublist. Recurse on the next bit. At each recursive call, we are given two
sublists and must respect the invariant that we pick one number from each
sublist. 

There are several implementation subtleties (handling empty lists at various
places, correct base case handling, deduplication, etc.) 
"""
class Solution:
    def find_maximum_xor(self, nums: List[int]) -> int:
        return self.solve_outer(nums, 31)
    
    def solve_outer(self, nums: List[int], k: int):
        """
        Wrapper function; k is the bit we are currently focusing on.
        """
        if k < 0:
            return 0
        nums0, nums1 = self.partition(nums, k)
        if not nums0:
            return self.solve_outer(nums1, k-1)
        if not nums1:
            return self.solve_outer(nums0, k-1)
        return (1 << k) + self.solve_inner(nums0, nums1, k-1)

    
    def solve_inner(self, nums0: List[int], nums1: List[int], k: int):
        # nums0 have 0 in some previous bit, nums1 have 1 in that bit
        # kth bit is the one we are now looking at. nums*0 have 0 in kth
        # bit, nums*1 have 1 in kth bit

        # If either nums0 or nums1 is empty, cannot choose one from each
        if not (nums0 and nums1):
            return 0
        
        # base case
        if k < 0:
            return 0
        
        nums00, nums01 = self.partition(nums0, k)
        nums10, nums11 = self.partition(nums1, k)

        # Our top priority (hard constraint) is making sure we pick one number
        # from nums0, one number from nums1. Our second priority is making sure 
        # the kth bits don't match
        if not nums00 and not nums10:
            #kth bits forced to match; proceed to (k-1)th bit
            return self.solve_inner(nums01, nums11, k-1)
        
        if not nums01 and not nums11:
            #kth bits forced to match; proceed to (k-1)th bit
            return self.solve_inner(nums00, nums10, k-1)
        
        #kth bits can't match. two choices for how
        return (1 << k) + max(
            self.solve_inner(nums00, nums11, k-1), 
            self.solve_inner(nums01, nums10, k-1)
        )
    
    def partition(self, nums: List[int], k: int) -> Tuple[List[int], List[int]]:
        """ 
        Returns two lists, nums0 and nums1. nums0 all have a 0 in the kth bit,
        nums1 all have a 1 in the kth bit, and everything before the kth bit
        is sliced off.
        """
        kth_bit_mask = (1 << k)
        slice_mask = (1 << (k+1)) - 1
        nums0 = [(num & slice_mask) for num in nums if not (num & kth_bit_mask)]
        nums1 = [(num & slice_mask) for num in nums if (num & kth_bit_mask)]
        return list(set(nums0)), list(set(nums1))
