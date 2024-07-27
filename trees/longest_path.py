from typing import List, Tuple
""" 
Basic idea:
First prune the tree of edges between nodes w same label.
Then for each node, define:
height(node): height of this node in the (pruned) subtree rooted at this node.
score(node): length of longest path in the (pruned) subtree rooted at this node

Both height and score can easily be calculated recursively from child heights.
Here we define the height of a leaf as 1, and of other nodes as 1 plus the max
height of any of its children in its (pruned) subtree.
"""
class Solution:
    def longest_path(self, parent: List[int], s: str) -> int:
        self.n = len(parent)
        self.parents = parent
        self.labels = s
        self.heights = [None for _ in range(self.n)]
        self.scores = [None for _ in range(self.n)]
        self.children = [[] for _ in range(self.n)]
        for child, parent in filter(
            lambda cp: cp[1] >= 0 and self.labels[cp[0]] != self.labels[cp[1]], enumerate(self.parents)):
            self.children[parent].append(child)
        for i in range(self.n):
            self.calculate_height(i)
        for i in range(self.n):
            self.calculate_score(i)
        return max(self.scores)
    
    def calculate_height(self, node: int) -> int:
        if self.heights[node] is None:
            child_heights = [self.calculate_height(child) for child in self.children[node]]
            self.heights[node] = (1 + max(child_heights)) if child_heights else 1
        return self.heights[node]
    
    def calculate_score(self, node: int) -> int:
        if self.scores[node] is None:
            child_heights = sorted([self.heights[child] for child in self.children[node]])
            if len(child_heights) <= 1:
                self.scores[node] = self.heights[node]
            else:
                self.scores[node] = 1 + child_heights[-1] + child_heights[-2]
        return self.scores[node]
