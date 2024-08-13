
"""
Problem Source: https://leetcode.com/problems/serialize-and-deserialize-binary-tree/description/
Level: LC Hard
Implement a class that serializes and deserializes a binary tree.

Solution: we use an pre-order traversal to serialize.
When deserializing, we need to keep track of where in the string we need to read
from next.
"""

# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

NULL_VAL = 1001

class Codec:
    def serialize(self, root):
        """Encodes a tree to a single string.
        
        :type root: TreeNode
        :rtype: str
        """
        if root:
            return str(root.val) + " " + self.serialize(
                root.left) + self.serialize(root.right)
        return str(NULL_VAL) + " "
        

    def deserialize(self, data):
        """Decodes your encoded data to tree.
        
        :type data: str
        :rtype: TreeNode
        """
        data_list = data.split(' ')
        return self.dsr_wrap(data_list, 0)[0]

    def dsr_wrap(self, data, idx) -> Tuple[TreeNode, int]:
        curr_val = int(data[idx])
        if curr_val == NULL_VAL:
            return None, idx+1
        curr_node = TreeNode(curr_val)
        left_tree, right_idx = self.dsr_wrap(data, idx+1)
        right_tree, next_idx = self.dsr_wrap(data, right_idx)
        curr_node.left = left_tree
        curr_node.right = right_tree
        return curr_node, next_idx
    