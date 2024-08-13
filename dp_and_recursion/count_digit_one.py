from typing import List

"""
Given an integer n, determine the total number of times the digit 1 appears in
all integers up to n.

Problem Source: https://leetcode.com/problems/number-of-digit-one/
Level: LC Hard

Basic idea:
Consider building a number m <= n. Fix the first digit. If the first digit
is strictly less than that of n, the subsequent digits can be anything. If the
first digits are equal, recurse on the remaining portion of n. 

Example: Suppose n = 6807.
If m is of the form 4***, then *** can be anything from 000 to 999.
The number of 1s that occur in [000...999] is the total number of digits that
occur divided by 10, i.e. 3 * 10^3 / 10 = 300. More generally, the number of 
digits in [000...10^m-1] is m * 10^(m-1).

If m is of the form 6***, then *** is at most 807, so recurse on 807.

Note there's a subtlety for numbers of the form 1*** - we need to count the 
leading one here as well, and the count for this will differ based on whether
n starts with a 1 or not.
"""
class Solution:
    def countDigitOne(self, n: int) -> int:
        return self.wrapper(self.to_digits(n))

    def wrapper(self, digits: List[int]) -> int:
        m, first_digit = len(digits), digits.pop(0)
        if m == 1:  # base case
            return int(first_digit > 0)

        if first_digit == 0:
            return self.wrapper(digits)
        elif first_digit == 1:
            # <1+leq(rem)> [lead count], 1+<leq(rem)> [rem count], 0+anything 
            rem = self.from_digits(digits)
            return (rem + 1) + self.g(m-1) + self.wrapper(digits)
        else:
            return first_digit * self.g(m-1) + 10 ** (m-1) + self.wrapper(digits)
        
    def g(self, m: int) -> int:
        """Number of 1s in {0, 1, ..., 10^m - 1}, i.e. nums with <= m digits."""
        return m * (10 ** (m-1))

    def to_digits(self, n: int) -> List[int]:
        return [int(d) for d in str(n)]

    def from_digits(self, digits: List[int]) -> int:
        return int("".join([str(d) for d in digits]))
        