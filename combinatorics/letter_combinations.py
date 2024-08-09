from collections import List 
import itertools 
"""
Problem Source: https://leetcode.com/problems/letter-combinations-of-a-phone-number/
Level: LC Medium

"""
class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        substrs = [self.letters(int(digit)) for digit in digits]
        result = []
        for comb in itertools.product(*substrs):
            result.append("".join(list(comb)))
        return result
    
    def letters(self, digit: int) -> str:
        base = ord('a') + (digit - 2) * 3 + (digit > 7)
        s = chr(base) + chr(base+1) + chr(base+2)
        if digit == 7 or digit == 9:
            s += chr(base+3)
        return s