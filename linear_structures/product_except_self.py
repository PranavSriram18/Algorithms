import itertools

import operator
from typing import List


"""
Given an array nums, return an array whose ith element is the product of all
entries of nums *except* nums[i]. The catch is that it's not allowed to use
the division operator.

Source: https://leetcode.com/problems/product-of-array-except-self
Level: LC Med

Basic idea: prefix and suffix products. Concretely:
ret[i] = prod(nums[0:i]) * (nums[i+1:])

So, let pfx[i] = prod(nums[0:i]), sfx[i] = prod(nums[i+1:]).
By symmetry we can construct sfx by just reversing process for pfx.
"""
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        pfx = list(itertools.accumulate(nums, operator.mul))
        pfx = [1] + pfx[:-1]

        sfx = list(itertools.accumulate(
            reversed(nums), operator.mul))
        sfx = [1] + sfx[:-1]
        sfx = list(reversed(sfx))

        return [a * b for a, b in zip(pfx, sfx)]