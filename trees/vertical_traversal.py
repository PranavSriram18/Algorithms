from collections import defaultdict
from typing import List, Optional

"""
Implement a vertical order traversal of a binary tree.
Full problem description: https://leetcode.com/problems/vertical-order-traversal-of-a-binary-tree/
Level: LC Hard

Basic idea:
Store map of col -> list of (row, node_val) pairs
each col sorted by row first, node_val second
recursively process nodes in the binary tree, then postprocess the map into
the return format.
"""

class TreeNode:
    """Definition for a binary tree node"""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def verticalTraversal(self, root: Optional[TreeNode]) -> List[List[int]]:
        self.cols = defaultdict(list)
        self.process(root, 0, 0)
        return self.extract_cols()

    def process(self, root: Optional[TreeNode], row: int, col: int) -> None:
        if not root:
            return
        self.cols[col].append((row, root.val))
        self.process(root.left, row+1, col-1)
        self.process(root.right, row+1, col+1)

    def extract_cols(self):
        shift = -min(col for col in self.cols.keys())
        max_col = max(col for col in self.cols.keys())
        result = [[] for _ in range(max_col+shift+1)] 
        for col, elems in self.cols.items():
            s_elems = sorted(elems)
            result[col+shift] = [e[1] for e in s_elems]
        return result

        
        