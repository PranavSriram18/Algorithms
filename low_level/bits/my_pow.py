"""
Implement x^n.

Source: https://leetcode.com/problems/powx-n/description
Level: LC Med

"""
class Solution:
    def myPow(self, x: float, n: int) -> float:
        if x == 0.:
            return 0

        if n < 0:
            return 1. / self.myPow(x, -n)

        if n == 0:
            return 1.

        result = 1.
        while n:
            result *= (x if (n & 1) else 1.)
            x *= x
            n >>= 1
        return result
    