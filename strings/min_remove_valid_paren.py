
"""
Given a string s, remove the minimum number of parentheses possible to make
the parentheses valid. 

Full description: https://leetcode.com/problems/minimum-remove-to-make-valid-parentheses/description
Level: LC Med

"""
class Solution:
    def minRemoveToMakeValid(self, s: str) -> str:
        # walk forward
        delta = 0  # num "(" minus num ")"
        to_delete_f = set()
        for i, ch in enumerate(s):
            if ch == "(":
                delta += 1
            if ch == ")":
                if delta > 0:
                    delta -= 1
                else:
                    to_delete_f.add(i)
        
        # walk backward
        delta = 0
        to_delete_b = set()
        for i, ch in ((j, s[j]) for j in range(len(s)-1, -1, -1)):
            if ch == ")":
                delta += 1
            if ch == "(":
                if delta > 0:
                    delta -= 1
                else:
                    to_delete_b.add(i)

        to_delete = to_delete_f | to_delete_b
        
        ret = [ch for i, ch in enumerate(s) if i not in to_delete]
        return "".join(ret)