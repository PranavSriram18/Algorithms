from typing import List
"""
Problem source: https://leetcode.com/problems/find-the-divisibility-array-of-a-string/
Level: LC Medium
Description: 
You are given a 0-indexed string word of length n consisting of digits,
and a positive integer m.

The divisibility array div of word is an integer array of length n such that:

div[i] = 1 if the numeric value of word[0,...,i] is divisible by m, or
div[i] = 0 otherwise.

Return the divisibility array of word.

Basic idea: iterate forward and keep track of the current value.
"""
class Solution:
    def divisibility_array(self, word: str, m: int) -> List[int]:
        n = len(word)
        result = [0] * n
        curr = 0
        for i in range(n):
            curr = (curr * 10 + ord(word[i]) - ord('0')) % m
            if (curr == 0):
                result[i] = 1
        return result

if __name__=="__main__":
    sol = Solution()
    print(sol.divisibility_array("209304933", 7))
