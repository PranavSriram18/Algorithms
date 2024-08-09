from collections import deque
from typing import List

"""
Given an undirected graph, represented as a list of edges, find the length of 
the shortest cycle, or return -1 if no cycles exist.

Source: (TODO)
Level: LC Hard

Basic idea:
Run a BFS on each vertex u to find the shortest path from u to itself. There
are two little tricks:
1. When encountering a back edge, say from v to x, we need to disregard this
back edge if x was the node that added v to the queue.
2. Say we are running a BFS from u, and we encounter a back edge from v to x,
and we're not in the case described above. Then, u --> v -> x --> u is *not*
necessarily a cycle, since the u --> v and x --> u paths may share edges. 
However, we can treat it as if it is, since the existence of this pseudo-cycle
guarantees the existence of a shorter cycle (without the shared edges), and
the min-reduction in the end handles this.
"""

LARGE_VAL = 10 ** 9 + 7
class Solution:
    def findShortestCycle(self, n: int, edges: List[List[int]]) -> int:
        self.nbrs = [[] for _ in range(n)]        
        self.build_nbrs(edges)
        self.n = n
        self.best = [LARGE_VAL for _ in range(n)]
        for i in range(n):
            self.run_bfs(i)
        res = min(self.best)
        return res if res != LARGE_VAL else -1

    def build_nbrs(self, edges):
        for u, v in edges:
            self.nbrs[u].append(v)
            self.nbrs[v].append(u)
    
    def run_bfs(self, i):
        q = deque([i])
        # track distance from i to node, which node added u to queue
        self.dists = [(-1 if j != i else 0) for j in range(self.n)]
        self.preds = [-1 for _ in range(self.n)]
        while q:
            curr_node = q.popleft()
            curr_dist = self.dists[curr_node]
            for nb in self.nbrs[curr_node]:
                if self.dists[nb] == -1:  # unvisited
                    self.dists[nb] = curr_dist + 1
                    self.preds[nb] = curr_node
                    q.append(nb)
                elif self.preds[curr_node] != nb:  # filter direct back-edges
                    self.best[i] = min(self.best[i], curr_dist + self.dists[nb] + 1)
