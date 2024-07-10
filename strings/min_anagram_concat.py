
""" 
Given a string s, determine the minimum possible length of a string t such that
s can be represented as the concatenation of anagrams of t.
Problem Source: https://leetcode.com/problems/minimum-length-of-anagram-concatenation/description/
Level: LC Medium

Basic idea:
For a given k, validating whether k works as the block length is O(n) by
building a frequency table. So just check each divisor of n for an O(nlogn)
algorithm.
"""
class Solution:
    ALPHABET_SZ = 26

    def minAnagramLength(self, s: str) -> int:
        n = len(s)
        divisors = self.divisors(n)
        for d in divisors:
            freqs = self.build_freqs(s, d)
            if self.validate_freq(freqs):
                return d

    def divisors(self, n: int):
        return [i for i in range(1, n+1) if n % i == 0]

    def build_freqs(self, s: str, d: int):
        # d is length of block
        # m x Alphabet table, where m is number of blocks (n/d)
        n = len(s)
        m = n // d
        freqs = [[0] * Solution.ALPHABET_SZ for _ in range(m)]
        for i, ch in enumerate(s):
            block = i // d
            pos = ord(ch) - ord('a')
            freqs[block][pos] += 1
        return freqs

    def validate_freq(self, freqs):
        return all(x == freqs[0] for x in freqs)
