import ast
#import astor
import operator
from typing import Any, Dict, List, Tuple, Union

import sys_prompt

def print_ast(node: ast.AST, indent: int = 0) -> None:
    """
    Print AST structure, showing nodes and important non-node attributes.
    Excludes metadata like line numbers.
    """
    prefix = "  " * indent
    
    # Get node type
    node_type = type(node).__name__
    
    # Handle special cases where we want to show non-node attributes
    extra_info = ""
    if isinstance(node, ast.Name):
        extra_info = f"(id='{node.id}')"
    elif isinstance(node, ast.Constant):
        extra_info = f"(value={repr(node.value)})"
    
    # Print node with any extra info
    print(f"{prefix}{node_type}{extra_info}")
    
    # Get all children using iter_child_nodes
    for child in ast.iter_child_nodes(node):
        print_ast(child, indent + 1)

class DoubleTransformer(ast.NodeTransformer):
    """
    A node transformer that doubles the constant values in the code.
    """
    def visit_Num(self, node):
        node.value *= 2
        return node

    def visit_Name(self, node):
        return node

    def generic_visit(self, node):
        return super().generic_visit(node)

def double_numbers(code: str) -> Tuple[ast.AST, str]:
    tree = ast.parse(code)
    transformer = DoubleTransformer()
    new_tree = transformer.visit(tree)
    ast.fix_missing_locations(new_tree)
    return new_tree, ast.unparse(new_tree)

def test_basic():
    """
    Write a simple python function that includes a binary operation and a 
    function call. Print the AST of the function.
    """
    code = """
def example():
    x = 5 + 3
    print(x)
"""
    tree = ast.parse(code)
    print("AST for example function:")
    print_ast(tree)

def test_double():
    code = "x = 5 + 3"
    new_tree, new_code = double_numbers(code)
    print(f"new code:\n {new_code}")
    print(f"new tree:\n")
    print_ast(new_tree)

class ConstantFoldTransformer(ast.NodeTransformer):
    """
    Transformer that:
    1. Folds constant expressions (e.g., '1 + 2' becomes '3')
    2. Converts augmented assignments to regular assignments
    """
    
    # Mapping of AST operator types to Python operator functions
    BINARY_OPS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.LShift: operator.lshift,
        ast.RShift: operator.rshift,
        ast.BitOr: operator.or_,
        ast.BitXor: operator.xor,
        ast.BitAnd: operator.and_,
    }
    
    def visit_BinOp(self, node: ast.BinOp) -> Union[ast.BinOp, ast.Constant]:
        """
        Visit binary operation nodes.
        If both operands are constants, compute the result.
        """
        # First visit child nodes
        self.generic_visit(node)
        
        # If both operands are constants, compute the result
        if (isinstance(node.left, ast.Constant) and 
            isinstance(node.right, ast.Constant) and 
            type(node.op) in self.BINARY_OPS):
            
            try:
                op_func = self.BINARY_OPS[type(node.op)]
                result = op_func(node.left.value, node.right.value)
                return ast.Constant(value=result)
            except Exception:
                # If computation fails (e.g., division by zero), return original node
                return node
                
        return node
    
def test_constant_fold():
    t = ConstantFoldTransformer()
    code = "x = 5 + 3"
    old_tree = ast.parse(code)
    print(f"old tree:\n")
    print_ast(old_tree)
    new_tree = t.visit(old_tree)
    ast.fix_missing_locations(new_tree)
    print(f"new code:\n {ast.unparse(new_tree)}")
    print(f"new tree:\n")
    print_ast(new_tree)

class StringJoinTransformer(ast.NodeTransformer):
    """
    Replaces instances of '+' between two strings with calls to the join method.
    """
    def visit_BinOp(self, node: ast.BinOp) -> Union[ast.BinOp, ast.Constant]:
        # first visit children
        self.generic_visit(node)
        # if binop is not '+' or '+=', return node
        if node.op != ast.Add:
            return node
        
        # if both operands are constant strings, replace with join
        if (isinstance(node.left, ast.Constant) and isinstance(
            node.right, ast.Constant) and isinstance(
                node.left.value, str) and isinstance(node.right.value, str)):
            
            # Create the empty string constant for join
            empty_str = ast.Constant(value="")
            
            # Create the join attribute access
            join_attr = ast.Attribute(
                value=empty_str,
                attr='join',
                ctx=ast.Load()
            )
            
            # Create the list of strings to join
            str_list = ast.List(
                elts=[node.left, node.right],
                ctx=ast.Load()
            )

             # Create the join call
            return ast.Call(
                func=join_attr,
                args=[str_list],
                keywords=[]
            )
        
        return node

if __name__ == "__main__":
    print("\nTesting basic AST")
    test_basic()
    print("\nTesting double numbers")
    test_double()
    print("\nTesting constant folding")
    test_constant_fold()
    
