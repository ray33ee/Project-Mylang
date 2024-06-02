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
        self.working_function = None
        self.working_class = None
        self.assigning = False
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


        self.traverse(node.body)

        # By this point an init function should be found. If not, we raise an error
        if node.name not in self.map:
            raise errors.ClassMissingInitException

        self.working_class = None


    def visit_FunctionDef(self, node):
        # If the function is a class constructor, traverse its body. Otherwise dont bother
        if node.name == "__init__" and self.working_class:
            self.working_function = node

            self.map[self.working_class.name] = OrderedDict()

            for s in node.body:
                print(s)

            self.traverse(node.body)

            self.working_function = None

    def visit_MonoAssign(self, node):
        self.assigning = True
        self.traverse(node.target)
        self.assigning = False

    def visit_Call(self, node):
        pass

    def visit_SelfMemberVariable(self, node):
        # If we are looking at an assignment in a class constructor
        if self.working_class and self.working_function.name == "__init__" and self.assigning:
            self.map[self.working_class.name][node.id] = None


