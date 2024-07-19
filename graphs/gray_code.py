from typing import List
"""
Given an integer n, return any valid n-bit gray code sequence.
Full problem description: https://leetcode.com/problems/gray-code/description/

Basic idea:
You can recursively construct Gray codes of length n as follows:
-> Take two copies of the code for length n-1, appending 0s to the first
copy and 1s to the second
-> Notice that copy0 and copy1 satisfy the adjacency property individually
-> Stitch them together: result = copy0 + reversed(copy1)
-> The end of copy0 and start of reversed(copy1) differ by 1 bit, as do the
end of reversed(copy1) and start of copy0
"""
class Solution:
    def grayCode(self, n: int) -> List[int]:
        if n == 1:
            return [0, 1]
        prev = self.grayCode(n-1)
        part0 = [x * 2 for x in prev]
        part1 = [x * 2 + 1 for x in reversed(prev)]
        return part0 + part1
    