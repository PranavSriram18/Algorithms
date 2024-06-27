from typing import List, Callable, TypeVar, Tuple, Optional

T = TypeVar('T')

class SegmentTree:
    """
    Implements a SegmentTree in Python.
    The nodes of the tree are stored linearly in an array of length 2 * m,
    where m is the smallest power of 2 geq n, and n is the length of the
    underlying data array.
    The root is at position 1. There are m-1 interior nodes and m leaf nodes.
    Interior nodes are {1, ..., m-1} and leaf nodes are {m, ..., 2*m-1}
    Each leaf node with idx k represents the single array element k-m
    Each interior node represents the union of segments of its children
    """

    def __init__(self, data: List[T], bin_op: Callable[[T, T], T]):
        """
        Initializes the members of the Segment Tree.
        """
        # size of underlying data array
        self.n = len(data)
        # smallest power of 2 geq n; number of leaf nodes
        self.m = 1 << (self.n - 1).bit_length()

        # pad data to length m
        padded_data = data + [None] * (self.m - self.n)
        
        # stores accumulated values for nodes in tree
        self.stree = [None] * (2 * self.m)

        # Mapping indices in stree to corresponding segments of data
        # idx_to_segment[i] returns the left and right endpoints (inclusive) of 
        # the segment represented by node i
        # Length is self.m as we don't explicitly store segments for leaves
        self.idx_to_segment = [None] * self.m

        # Handle None elements in bin_op. Arguments will never both be None
        def wrapped_bin_op(x: Optional[T], y: Optional[T]) -> T:
            if x is None:
                return y  # type: ignore
            if y is None:
                return x
            return bin_op(x, y)
        self.bin_op = wrapped_bin_op

        self.populate_stree(1, padded_data)
        self.populate_idx_to_segment(1)

    def query(self, qleft: int, qright: int) -> T:
        return self.query_wrapper(1, qleft, qright)

    def populate_stree(self, node: int, data: List[Optional[T]]) -> T:
        if self.is_leaf(node):
            self.stree[node] = data[node - self.m]
        else:
            left_val = self.populate_stree(self.lc(node), data)
            right_val = self.populate_stree(self.rc(node), data)
            self.stree[node] = self.bin_op(left_val, right_val)
        return self.stree[node]
        
    def populate_idx_to_segment(self, node: int) -> Tuple[int, int]:
        if self.is_leaf(node):
            return (node - self.m, node - self.m)
        # The segment for a non-leaf is the union of segments of its children
        left, _ = self.populate_idx_to_segment(self.lc(node))
        _, right = self.populate_idx_to_segment(self.rc(node))
        self.idx_to_segment[node] = (left, right)
        return self.idx_to_segment[node]
    
    def query_wrapper(self, node: int, qleft: int, qright: int) -> T:
        left_left, right_right = self.segment(node)
        # Case 1: query completely overlaps with this node 
        if qleft == left_left and qright == right_right:
            return self.stree[node]
        
        left_node = self.lc(node)
        right_node = self.rc(node)
        _, left_right = self.segment(left_node)
        right_left, _ = self.segment(right_node)
        # 3 other cases: query contained in left subtree, 
        # query contained in right subtree, and query overlaps both subtrees
        if qright <= left_right:
            return self.query_wrapper(left_node, qleft, qright)
        elif qleft >= right_left:
            return self.query_wrapper(right_node, qleft, qright)
        else:
            result_left = self.query_wrapper(left_node, qleft, left_right)
            result_right = self.query_wrapper(right_node, right_left, qright)
            return self.bin_op(result_left, result_right)
        
    def update(self, idx: int, value: T) -> T:
        node = idx + self.m
        self.stree[node] = value
        node = self.parent(node)
        while (node >= 1):
            self.stree[node] = self.bin_op(
                self.stree[self.lc(node)], self.stree[self.rc(node)])
            node = self.parent(node)
        return value
        
    # Helpers
    def segment(self, node: int) -> Tuple[int, int]:
        if self.is_leaf(node):
            return (node - self.m, node - self.m)
        return self.idx_to_segment[node]
    
    def lc(self, node: int) -> int:
        return 2 * node
    
    def rc(self, node: int) -> int:
        return 2 * node + 1
    
    def parent(self, node: int) -> int:
        return node // 2
    
    def is_leaf(self, node: int) -> bool:
        return node >= self.m
