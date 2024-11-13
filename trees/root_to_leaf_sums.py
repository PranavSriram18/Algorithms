from typing import List, Optional

"""

Problem statement:
You are given the root of a binary tree containing digits from 0 to 9 only.

Each root-to-leaf path in the tree represents a number.

For example, the root-to-leaf path 1 -> 2 -> 3 represents the number 123.
Return the total sum of all root-to-leaf numbers.

Source: https://leetcode.com/problems/sum-root-to-leaf-numbers/description
Level: LC Medium

Basic Idea:
Recursion. visit(node) returns the sum of all paths that pass through that node,
i.e. the sum of all paths with leaves in the subtree of that node.
"""

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def sum_numbers(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        return self.visit(root, [])

    def visit(self, node, prefix: List[int]) -> int:
        new_pfx = prefix + [node.val]
        if node.left and node.right:
            return self.visit(
                node.left, new_pfx) + self.visit(node.right, new_pfx)
        elif node.left:
            return self.visit(node.left, new_pfx)
        elif node.right:
            return self.visit(node.right, new_pfx)
        else:
            return int("".join([str(d) for d in new_pfx]))
        