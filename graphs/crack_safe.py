from collections import deque
from typing import List

""" 
Scratch:
We model this problem as finding an Eulerian circuit in the following directed
graph.
Nodes: all strings of length (n-1) [k^(n-1) nodes.
Edges: [a0 a1 ... a_{n-2}] has an out edge to [a1 a2 ... a_{n-1}] for each of
the k possible values of a_{n-1}.
Out edge representation: for each node, there are k out edges, based on
the digit we append, so can maintain a list of size k for each node to track used
out edges.

Regularity: each edge has same in-degree and out-degree; thus whenever we enter
a non-initial node we can always continue the path.
"""
class Solution:
    def crack_safe(self, n: int, k: int) -> str:
        if n == 1:
            # edge case - just concat all digits
            return "".join([str(i) for i in range(k)])
        self.n = n
        self.k = k
        self.create_graph()
        q = deque()
        q = self.find_euler_path(q)
        return self.create_code(q)

    def create_graph(self):
        self.nodes = self.construct_nodes(self.n-1)
        self.node_to_id = {node : i for i, node in enumerate(self.nodes)}
        self.edges = [[1 for _ in range(self.k)] for _ in self.nodes]

    def construct_nodes(self, m: int) -> List[str]:
        """ 
        Recursively generates all strings of length m, with digits in [0, k)
        """
        if m == 0:
            return [""]
        partial_nodes = self.construct_nodes(m-1)
        return [p + str(i) for i in range(self.k) for p in partial_nodes]
    
    def find_euler_path(self, q: deque[str]) -> deque[str]:
        """
        The algorithm maintains two key pieces of state:
        q: The circuit formed so far. 
        self.edges: Maintains which edges remain available to traverse.
        Invariant: q is always "closed", e.g. of the form (a b c d a) 
        instead of (a b c d), i.e. q[-1] == q[0]. Exception is when q is
        empty.
        """
        #print(f"\nIn find_euler_path; current circuit length is {len(q)}")
        # Termination case
        if len(q) == self.k ** self.n + 1:  # TODO - check off by 1
            return q
        
        # Initialization case
        if not q:
            q.append(self.nodes[0])
        
        # Rotate current circuit so that it ends with a node we can start from
        # Maintain invariant that q[0] == q[-1]
        while not self.has_edges(q[-1]):
            q.pop()
            q.appendleft(q[-1])

        curr_node = q[-1]
        found_next = True
        while found_next:
            out_edges = self.get_edges(curr_node)
            found_next = False
            for i, avail in enumerate(out_edges):
                if avail:
                    curr_node = self.neighbor(curr_node, i)
                    q.append(curr_node)
                    found_next = True
                    out_edges[i] = False
                    break
        
        # when we reach here, we have completed a circuit
        return self.find_euler_path(q)
    
    def create_code(self, q: deque[str]) -> str:
        #print(f"Queue is: {q}")
        code = q.popleft()
        for w in q:
            code += w[-1]
        return code

    def get_edges(self, node: str):
        """ 
        List of 0/1 indicating if out edges for the given node are still
        available.
        """
        return self.edges[self.node_to_id[node]]
    
    def has_edges(self, node: str):
        return any(self.get_edges(node))
    
    def neighbor(self, node: str, i: int):
        return node[1:] + str(i)

if __name__=="__main__":
    s = Solution()
    print(s.crack_safe(n=2, k=2))
    print(s.crack_safe(n=3, k=4))