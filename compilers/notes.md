## Multiprocessing
Use multiprocesing.Manager for complex shared data.
mp.Pool creates pool; use 'with' and pool.map(function, chunks).
pool can't handle lambdas; can use partial to fix parameters.

### Value Sharing with Multiprocessing

Use multiprocessing.Value and multiprocessing.Array to share data between processes.
with v.get_lock():  # context-managed lock
    v.value += 1

Example:

from multiprocessing import Value, Array

def worker(shared_num, shared_arr):
    # shared_num and shared_arr are synchronized
    with shared_num.get_lock():
        shared_num.value += 1
    
    shared_arr[0] = 42

if __name__ == '__main__':
    num = Value('i', 0)  # Shared integer
    arr = Array('i', [0, 0, 0])  # Shared array
    p = Process(target=worker, args=(num, arr))
    p.start()
    p.join()


### Performance and Profiling
Use trace to get program trace.
Use cProfile to get call graph and breakdown of time spent in each function.

## ASTs
At a high level:
0. Each node in AST is an instance of a subclass of ast.AST.
1. Children of a node are either attributes, or elements in lists (in which case the list is an attribute).
2. Nodes can have different types, like Module (the root node), BinOp, etc. They all inherit from AST
3. 'Module' nodes will always have 'body' as an attribute. Other node types have different attributes, like BinOp always has 'left' and 'right'
4. To properly traverse an AST, we need to inspect the types of the nodes, and figure out what attributes they contain
5. Not all attributes of nodes are themselves nodes; can filter during traversal using:
isinstance(attr, ast.AST) or isinstance(attr, list).

### Traversing ASTs
ast.iter_child_nodes(node) yields all children of node.
ast.walk(node) yields all descendants of node (no guarantees on order; uses DFS).

**Visitor Base Classes**
ast.NodeVisitor: Base class for read-only traversal

Provides visit(node) which dispatches to appropriate visit_NodeType methods
Provides generic_visit(node) which visits all children of a node
You subclass this and implement visit_X methods for nodes you care about
Default behavior is to traverse entire tree via generic_visit
Unlike walk(), the visitors traverse in a predictable order and give you 
hooks for preprocessing/postprocessing nodes.

ast.NodeTransformer: Subclass of NodeVisitor for modifying trees
Like NodeVisitor but visit methods can return nodes to replace the visited node
If they return None, the node is removed
Commonly used for AST transformations

**Transformer Patterns**
ast.parse(code), ast.unparse(node): code <--> AST
need ast.fix_missing_locations(node) after transforming AST before unparsing

transformer.visit(node) visits node and all descendants, allowing you to modify nodes
transformer.generic_visit(node) visits all children of node, allowing you to modify them
transformer.visit_X(node) allows you to modify node of type X


### Pitfalls
1. Assuming all nodes have certain attributes (like 'body' or 'value')
2. Not checking node types before accessing attributes
3. Forgetting to traverse child nodes
4. Assuming lists of children are always non-empty

## Notes on Python ASTs

### Basic Primitives

**Core AST Node Types**
Module: Top-level node for a Python file
FunctionDef: Function definitions
Name: Variable names
Constant: Literal values
BinOp: Binary operations
Call: Function calls
Assign: Assignment statements
For/While: Loop constructs
If: Conditional statements

**Node Properties**
_fields: Child nodes
_attributes: Node attributes
lineno, col_offset: Source location info
Context types (Load/Store/Del)

**Visitor Pattern**
NodeVisitor: For analysis
NodeTransformer: For modifications
visit_* methods for specific node types

**Common Transformations**
Adding/removing nodes
Modifying existing nodes
Constant folding
Expression simplification
