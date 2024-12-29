import ast
#import astor
from typing import Any, Dict, List

import sys_prompt

def print_ast(node: ast.AST, level: int = 0) -> None:
    indent = '  ' * level
    node_type = type(node).__name__

    # get attributes that aren't children
    attrs = {
        name: getattr(node, name) for name in node._attributes + node._fields if hasattr(
            node, name
        ) and not isinstance(getattr(node, name), ast.AST) and not isinstance(
            getattr(node, name), list
        )
    }

    print(f"{indent}{node_type}: {attrs}")

    # recurse
    for name, value in ast.iter_fields(node):
        if isinstance(value, list):
            for cnode in value:
                if isinstance(cnode, ast.AST):
                    print_ast(cnode, level+1)
        elif isinstance(value, ast.AST):
            print_ast(value, level+1)

def explore_ast(node: ast.AST, indent: int = 0) -> None:
    """Explore AST nodes with detailed information"""
    prefix = "  " * indent
    node_type = type(node).__name__
    
    # Get important attributes
    attrs = {}
    for attr in node._attributes + node._fields:
        if hasattr(node, attr):
            value = getattr(node, attr)
            if isinstance(value, (str, int, float, bool)):
                attrs[attr] = value
            elif isinstance(value, ast.AST):
                attrs[attr] = f"<{type(value).__name__}>"
    
    print(f"{prefix}{node_type}: {attrs}")
    
    # Recurse into children
    for child_name, child in ast.iter_fields(node):
        if isinstance(child, list):
            for item in child:
                if isinstance(item, ast.AST):
                    explore_ast(item, indent + 1)
        elif isinstance(child, ast.AST):
            explore_ast(child, indent + 1)
            
def analyze_additions(code: str) -> Dict:
    """
    Analyze addition operations in the code.
    
    Return a dictionary containing:
    - numeric_adds: count of numeric additions
    - string_adds: count of string concatenations
    - locations: list of line numbers where additions occur
    """
    tree = ast.parse(code)
    results = {
        'numeric_adds': 0,
        'string_adds': 0,
        'locations': []
    }

    def analyze_node_type(cnode: ast.AST) -> str:
        if isinstance(cnode, ast.Constant):
             # look at the type of the contained value
            return type(cnode.value).__name__
        elif isinstance(cnode, ast.Name):
            # AST variables
            # Search for assignments to this variable name
            var_name = cnode.id
            for assign_node in ast.walk(tree):
                if isinstance(assign_node, ast.Assign):
                    for target in assign_node.targets:
                        if isinstance(target, ast.Name) and target.id == var_name:
                            # Found an assignment, analyze the value
                            return analyze_node_type(assign_node.value)
            return 'unknown'  # Variable type couldn't be determined
        elif isinstance(cnode, ast.Call):
            # function call
            pass  # TODO
        elif isinstance(node, ast.BinOp):
            # recurse
            return analyze_node_type(cnode.left)
        else:
            pass

    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            results['locations'].append(node.lineno)
            key = 'string_adds' if analyze_node_type(
                node.left) == 'str' else 'numeric_adds'
            results[key] += 1

    # Your code here!
    # Hints:
    # - Use ast.walk(tree) to traverse
    # - Check for ast.BinOp nodes with ast.Add operations
    # - Look at node.left and node.right to determine operand types
    # - node.lineno will give you line numbers
    
    return results

def test_analyze_additions():
    # Test your implementation
    test_code = """
    x = 1 + 2        # numeric
    y = "a" + "b"    # string
    z = 3 + (4 + 5)  # nested numeric
    """

    results = analyze_additions(test_code)
    print("Results:", results)


def main():
    code1 = """
def add(a, b):
    return a + b
"""

    tree1 = ast.parse(code1)
    print("basic function ast: \n")
    print_ast(tree1)

    print("exploring AST: \n")
    explore_ast(tree1)

if __name__=="__main__":
    main()