from typing import List 

"""
Given a nonnegative decimal number num, return the largest number that can be
formed by swapping two digits of num.

Source: https://leetcode.com/problems/maximum-swap
Level: LC Medium

Basic idea:
There are two cases. Either the first digit is not the largest, in which case
we want to swap it with the last occurrence of the largest digit. Or, if the
first digit is largest, simply recurse on the rest of the number.

Time complexity is O(log(n)^2)
"""
class Solution:
    def maximumSwap(self, num: int) -> int:
        # get digits as list of int
        digits = [int(d) for d in str(num)]
        swapped_digits = self.solve(digits)
        return int("".join([str(d) for d in swapped_digits]))

    def solve(self, digits: List[int]):
        k = len(digits)
        if k == 0:
            return []

        # identify the largest digit
        max_digit = max(digits)

        if digits[0] != max_digit:
            # identify the last occurrence of the largest digit
            max_digit_pos = next(
                i for i in range(k-1, -1, -1) if digits[i] == max_digit
            )
            # swap first and largest digit
            digits[0], digits[max_digit_pos] = digits[max_digit_pos], digits[0]
            return digits
        else:
            # recurse on remaining digits
            return [digits[0]] + self.solve(digits[1:])
