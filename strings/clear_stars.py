import heapq
""" 
Problem Statement:
You are given a string s. It may contain any number of '*' characters. 
Your task is to remove all '*' characters.

While there is a '*', do the following operation:

Delete the leftmost '*' and the smallest non-'*' character to its left. If 
there are several smallest characters, you can delete any of them.
Return the lexicographically smallest resulting string after removing all '*'
characters.
"""
class Solution:
    def clear_stars(self, s: str) -> str:
        removed_idxs = set()
        # min-heap sorted by char ascending, position descending
        pq = []
        for i, ch in enumerate(s):
            if ch != '*':
                heapq.heappush(pq, (ch, -i))
            else:
                popped_ch, neg_popped_idx = heapq.heappop(pq)
                removed_idxs.add(i)
                removed_idxs.add(-neg_popped_idx)
        remaining_chars = [ch for i, ch in enumerate(s) if i not in removed_idxs]
        return "".join(remaining_chars)