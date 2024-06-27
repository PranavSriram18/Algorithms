from typing import List 
from collections import defaultdict

"""
Source: https://leetcode.com/problems/pyramid-transition-matrix/
Level: LC Medium
See source for full problem description.

Basic idea: brute force depth first search.
State is parameterized by:
* previous row
* position in current row
* previous characters in current row
"""
class Solution:
    def pyramid_transition(self, bottom: str, allowed: List[str]) -> bool:
        self.build_trans_table(allowed)
        return self.solve(bottom, 0, "")

    def build_trans_table(self, allowed):
        self.trans_table = defaultdict(list)
        for a, b, c in allowed:
            self.trans_table[a+b].append(c)

    def solve(self, prev_row, curr_pos, curr_row_so_far):
        k = len(prev_row)

        # Base case 0: if k == 1, finished the pyramid
        if k == 1:
            return True

        # if curr_pos == k-1, we've reached end of row; move to next
        if curr_pos == k-1:
            return self.solve(curr_row_so_far, 0, "")

        # dfs: recursively try each allowed char 
        for ch in self.trans_table[prev_row[curr_pos:curr_pos+2]]:
            if self.solve(prev_row, curr_pos+1, curr_row_so_far+ch):
                return True
        return False

if __name__=="__main__":
    sol = Solution()
    print(sol.pyramid_transition("BCD", ["BCC","CDE","CEA","FFF"]))
    