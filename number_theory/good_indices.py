from typing import List

"""
Problem description: 
https://leetcode.com/problems/double-modular-exponentiation/description/
Level: LC medium

Basic idea: optimize the (a^b % 10) part using Euler's theorem.
a^5 ~ a mod 10 
"""
class Solution:
    def get_good_indices(self, variables: List[List[int]], target: int) -> List[int]:
        self.vars = variables
        self.n = len(self.vars)
        self.target = target
        return [idx for idx in range(self.n) if self.is_good(idx)]

    def is_good(self, idx):
        a, b, c, m = self.vars[idx]
        return (self.raise_mod_10(a, b) ** c) % m == self.target

    def raise_mod_10(self, a, b):
        return (a ** (((b-1) % 4) + 1)) % 10
    