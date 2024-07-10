from typing import List 

"""
Problem Statement (condensed): 
You are given two arrays with positive integers arr1 and arr2.
Return the length of the longest common prefix among all pairs. 
If no common prefix exists among them, return 0.

Problem Source: https://leetcode.com/problems/find-the-length-of-the-longest-common-prefix/description/
Level: LC Medium

Basic Idea:
Naive approach is O(n^2) by comparing each pair
Instead, generate all prefixes of arr1, arr2 and take the set intersection
"""
class Solution:
    def longest_common_prefix(self, arr1: List[int], arr2: List[int]) -> int:
        pfxs_1 = self.prefixes(arr1)
        pfxs_2 = self.prefixes(arr2)
        common_pfxs = pfxs_1 & pfxs_2
        common_lengths = [len(x) for x in common_pfxs]
        return max(common_lengths) if common_lengths else 0

    def prefixes(self, arr: List[int]) -> set[str]:
        result = set()
        for val in arr:
            s = str(val)
            result.update(s[0:i] for i in range(len(s)))
        return result
