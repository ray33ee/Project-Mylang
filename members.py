import ast
from collections import OrderedDict

import custom_nodes
import errors


def resolve_members(node: ast.AST):
    m = Members()
    m.visit(node)
    return m.get_members()

# Visitor class used to extract the member variable names for each class in ast
class Members(ast.NodeVisitor):
    def __init__(self):
        self.working_class = None
        self.map = {}

    # Convert the dictonary of class,ordered dict pairs into a dictionary of class,list pairs
    def get_members(self):
        return {key: list(value) for key, value in self.map.items()}

    def traverse(self, node):
        if isinstance(node, list):
            for n in node:
                self.visit(n)
        else:
            self.visit(node)

    def visit_ClassDef(self, node):
        self.working_class = node

        if node.name in self.map:
            raise "Duplicate class declarations"

        self.map[node.name] = OrderedDict()

        self.traverse(node.body)

        self.working_class = None

    def visit_InitFunctionDef(self, node):

        self.traverse(node.body)

        # Add the list of member variables to the InitFunctionDef. This is used to Rustify ir.InitFunctionDef
        node.member_list = list(self.map[self.working_class.name].keys())

    def visit_InitAssign(self, node):
        self.map[self.working_class.name][node.id] = None


