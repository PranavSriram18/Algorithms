import bisect 
from typing import List
"""
A strobogrammatic number is a number that looks the same when looked at upside 
down.

Given two strings low and high that represent two integers low and high where 
low <= high, return the number of strobogrammatic numbers in the range 
[low, high].

Source: https://leetcode.com/problems/strobogrammatic-number-iii/description/
Level: LC Hard

Basic ideas:
1. Obviously can represent as f(high) - f(low-1), where f(n) is number of S-numbers
in [0, ..., n]. 

2. Recursion by fixing the first digit. When we fix the first digit, the last is
also fixed, and we need to recurse over the middle. There are a couple
subtleties in handling the middle, listed below.

3. If first digits are equal and fixed last digit is greater than argument's
last digit, then we need to recurse over mid-1. 

4. When converting mid or (mid-1) to an int, we need to make sure we aren't 
silently dropping a leading zero.

5. More generally, a lot of the pain in this problem comes from cleanly handling
leading zeroes in various places.
"""
class Solution:
    def strobogrammaticInRange(self, low: str, high: str) -> int:
        hi, lo_m_1 = self.to_digits(int(high)), self.to_digits(int(low)-1)
        return self.f(hi, False) - self.f(lo_m_1, False)

    def f(self, digits: List[int], allow_leading_zero: bool) -> int:
        k = len(digits)
        n = self.from_digits(digits)
        # base cases: f(-1) = 0, f(0) = 1, f(1...7) = 2, f(8..9) = 3 
        if k <= 1:
            return bisect.bisect_right([-1, 0, 1, 8], n) - 1

        d0, d_last = digits[0], digits[-1]
        pairs = {0:0, 1:1, 6:9, 8:8, 9:6}
        mid_digits = digits[1:k-1]
        mid = self.from_digits(mid_digits)

        def contrib(d):
            """
            Four cases regarding starting with digit d:
            Not allowed, totally free, recurse on mid, recurse on mid-1
            """
            if d0 == d:
                return (
                    self.f(mid_digits, True) if d_last >= pairs[d] else self.f(self.to_digits(mid-1, k-2), True))
            return 0 if d0 < d else self.g(k-2)
        
        # in the first call, we need to handle starting at a later position
        zero_contrib = contrib(0) if allow_leading_zero else self.h(k-1)
        start_digits = (1, 6, 8, 9)
        return zero_contrib + sum(contrib(d) for d in start_digits)

    def to_digits(self, n: int, k: int|None = None) -> List[int|str]:
        """
        Converts an int n to a list of integer digits.
        If k is specified, left-pads with 0s so result is of length k.
        Special case is n=-1, in which case ["*"] is returned.
        """
        if n < 0:
            return ["*"]
        res = [int(d) for d in str(n)]
        return [0] * ((k - len(res)) if k else 0) + res

    def from_digits(self, digits: List[int|str]) -> int:
        if digits == ["*"]:
            return -1
        return int("".join([str(d) for d in digits])) if digits else 0

    def g(self, k: int) -> int:
        """
        Number of S-numbers with exactly k digits, leading 0s allowed.
        We have 5 degrees of freedom for each of first k/2 digits, and if k is
        odd, 3 degrees of freedom for the middle digit.
        """
        return (5 ** (k // 2)) * (3 ** (k % 2))

    def h(self, k: int):
        """Number of S-numbers with up to k digits, leading 0s not allowed."""
        return self.f(self.to_digits(10 ** k - 1), False)
