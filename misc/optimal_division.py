from typing import List

""" 
Problem Source: https://leetcode.com/problems/optimal-division/
Level: LC Medium
"""
class Solution:
    def optimal_division(self, nums: List[int]) -> str:
        if len(nums) == 1:
            return str(nums[0])
        elif len(nums) == 2:
            return str(nums[0]) + "/" + str(nums[1])
        result = str(nums[0]) + "/("
        result += "/".join([str(x) for x in nums[1:]])
        result += ")"
        return result
    