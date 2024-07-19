
""" 
Problem Source: https://leetcode.com/problems/zigzag-conversion/
Level: LC Medium
Basic idea:
Maintain a list of num_rows strings, and keep track of two pieces of State:
current row and direction.
"""
class Solution:
    def convert(self, s: str, num_rows: int) -> str:
        n = len(s)
        if num_rows == 1:
            return s
        char_lists = [[] for _ in range(num_rows)]
        curr_row = 0
        curr_dir = 1
        for ch in s:
            char_lists[curr_row].append(ch)
            curr_row = curr_row + curr_dir
            if 0 < curr_row < num_rows - 1:
                continue
            curr_dir = -1 if curr_row else 1
        return "".join(["".join(x) for x in char_lists])
    