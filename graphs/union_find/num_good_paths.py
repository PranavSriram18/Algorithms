from typing import List

"""
Source: https://leetcode.com/problems/number-of-good-paths/description/
Level: LC Hard

Abridged description: Given a Tree T, count the number of good paths.
A good path is a path that starts and ends at nodes with equal values, and with
each intermediate value not exceeding the endpoint values.

Solution:
I really liked this problem. There are a few key ideas involved.

Idea 1: Each candidate starting point for a path induces a subforest, by 
considering edges only among vertices with values not exceeding the start value.
We can use a UnionFind to represent this forest.

Idea 2: Process candidate starting points in increasing order of value. Then,
we only need a single UnionFind structure as we only ever add and never remove
edges.

Idea 3: Once we've sorted nodes, when processing nodes[i] we're adding a bunch
of edges (i, j) where j < i. Each edge addition potentially merges some UF
components. Due to the possibility of several nodes having equal values, there
could be multiple new valid paths formed. 

Idea 4: Augment the UnionFind to track the max value and number of occurrences
in each component, as well as the total valid paths. When merging components,
we update the total based on the number of occurrences of the running max in
both components. The main interesting case is when both components have the
same max value.
"""

class AugmentedUnionFind:
    def __init__(self, n: int, vals: List[int]):
        self.parents = list(range(n))
        self.sizes = [1 for _ in range(n)]
        self.vals = vals
        # max_val, count in each connected component
        self.max_in_cc = [(val, 1) for val in vals]
        self.total_paths = n

    def repr(self, u):
        if self.parents[u] != u:
            self.parents[u] = self.repr(self.parents[u])
        return self.parents[u]

    def add_edge(self, u, v):
        urep, vrep = self.repr(u), self.repr(v)
        if urep != vrep:
            u_max, u_count = self.max_in_cc[urep]
            v_max, v_count = self.max_in_cc[vrep]
            new_max_ct = (u_max, u_count) if u_max > v_max else (
                (v_max, v_count) if v_max > u_max else (u_max, u_count+v_count)
            )
            if u_max == v_max:
                self.total_paths += u_count * v_count
            small, large = (urep, vrep) if (self.sizes[urep] < self.sizes[vrep]) else (vrep, urep)
            self.parents[small] = large
            self.sizes[large] += self.sizes[small]
            self.max_in_cc[large] = new_max_ct

    def num_max_in_cc(self, u):
        return self.max_in_cc[self.repr(u)][1]

class Solution:
    def numberOfGoodPaths(self, vals: List[int], edges: List[List[int]]) -> int:
        self.n = len(vals)
        self.vals = vals
        self.uf = AugmentedUnionFind(self.n, vals)

        # sort nodes in increasing order of value
        self.nodes = sorted(range(self.n), key=lambda i: (vals[i], i))
        self.build_edges(edges)
        for u in self.nodes:
            for v in self.edges[u]:
                self.uf.add_edge(u, v)
        return self.uf.total_paths
            
    def build_edges(self, edges):
        self.edges = [[] for u in range(self.n)]
        for u, v in edges:
            small, large = (u, v) if (self.vals[u], u) < (self.vals[v], v) else (v, u)
            self.edges[large].append(small)
