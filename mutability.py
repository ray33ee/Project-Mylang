import ast
from functools import reduce
import ir


def fill_mutability(node, table):
    m = _Mutability(table)
    return m.visit(node)


# Returns true if the node contains a setter
class _Mutability(ast.NodeVisitor):

    def __init__(self, table):
        pass

    def visit(self, node):

        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        res = visitor(node)
        return res

    def generic_visit(self, node):
        for field, value in ast.iter_fields(node):
            if isinstance(value, list) or isinstance(value, ast.AST):
                if self.traverse(value) == True:
                    return True
        return False

    def traverse(self, node):
        if type(node) is list:
            return reduce(lambda x, y : x or self.traverse(y), node, False)
        else:
            return self.visit(node)

    def visit_ClassDef(self, node):
        node.mutable = self.traverse(node.functions)
        return node.mutable


    def visit_Reassign(self, node):
        if type(node.target) is ir.SelfVariable:
            return True

        return False
