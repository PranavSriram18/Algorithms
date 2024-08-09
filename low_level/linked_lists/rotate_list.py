from typing import Optional, Tuple

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
        
class Solution:
    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        l = self.length(head)
        k = k % l
        break_node, last_node = self.get_nodes(head, k)
        last_node.next = head
        new_first_node = break_node.next
        break_node.next = None
        return new_first_node
    
    def get_nodes(self, head: Optional[ListNode], k: int) -> Tuple[ListNode, ListNode]:
        