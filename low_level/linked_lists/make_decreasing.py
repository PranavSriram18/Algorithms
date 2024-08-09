
from typing import List, Optional

"""
Given a linked list, remove all nodes for which there exists a greater value to
the right of the node. 

Basic idea - 2 stacks. 
Push everything into a left stack
Start popping into a right stack, tracking best seen so far
Only stuff that improves best gets pushed onto right stack
Build new linked list from right stack
"""

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
        
class Solution:
    def removeNodes(self, head: Optional[ListNode]) -> Optional[ListNode]:
        self.build_left_stack(head)
        self.build_right_stack()
        return self.extract_list()

    def build_left_stack(self, head: Optional[ListNode]):
        self.left_stack = []
        curr = head
        while curr:
            self.left_stack.append(curr)
            curr = curr.next

    def build_right_stack(self):
        max_val = -1
        self.right_stack = []
        while self.left_stack:
            node = self.left_stack.pop()
            if node.val >= max_val:
                self.right_stack.append(node)
                max_val = node.val

    def extract_list(self) -> Optional[ListNode]:
        if not self.right_stack:
            return None
        head = self.right_stack.pop()
        curr = head
        while self.right_stack:
            curr.next = self.right_stack.pop()
            curr = curr.next
        curr.next = None
        return head
        