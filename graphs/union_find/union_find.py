from typing import List

class UnionFind:
    """ 
    Implements a UnionFind structure with path compression 
    and union by size in Python.
    The data structure maintains two key pieces of state: 
    self.parents tracks the parent of each node, which is initially itself.
    self.sizes tracks the size of the component of each representative.
    """
    def __init__(self, n):
        self.n = n
        self.parents = [i for i in range(n)]
        self.sizes = [1 for _ in range(n)]

    def representative(self, u: int) -> int:
        if self.parents[u] == u:
            return u
        self.parents[u] = self.representative(self.parents[u])
        return self.parents[u]
    
    def is_repr(self, u: int) -> bool:
        return self.parents[u] == u
    
    def connected(self, u: int, v: int) -> bool:
        return self.representative(u) == self.representative(v)
    
    def add_edge(self, u: int, v: int) -> None:
        if self.connected(u, v):
            return
        u_rep, v_rep = self.representative(u), self.representative(v)
        # merge smaller into larger
        smaller, larger = (u_rep, v_rep) if self.sizes[
            u_rep] < self.sizes[v_rep] else (v_rep, u_rep)
        self.parents[smaller] = larger
        self.sizes[larger] += self.sizes[smaller]

    def component_sizes(self) -> List[int]:
        return [self.sizes[r] for r in filter(
            lambda x: self.parents[x] == x, range(self.n))]
    
    def connected_components(self) -> List[List[int]]:
        """
        Returns a list of all the connected components. Each entry is a list of
        nodes. The length of the returned list is the number of connected
        components.
        """
        reprs = [x for x in range(self.n) if self.is_repr(x)]
        r2i = {x:i for i, x in enumerate(reprs)}
        result = [[] for _ in reprs]
        for u in range(self.n):
            result[r2i[self.representative(u)]].append(u)
        return result


