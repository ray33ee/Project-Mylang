import ast
from functools import reduce
import ir


def fill_mutability(node, table):
    m = _Mutability(table)
    m.visit(node)
    return m.cache

# Recursively visit nodes to determine if member functions and classes are mutable or immutable
class _Mutability(ast.NodeVisitor):

    def __init__(self, table):
        self.table = table
        self.class_table = None

        self.cache = {}

    def visit(self, node):

        print(ast.dump(node))

        if type(node) is ir.SelfFunction:
            if node.id in self.cache:
                return self.cache[node.id]

        if isinstance(node, ir.MemberFunctionDef):
            if node.name in self.cache:
                return self.cache[node.name]

        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        res = visitor(node)

        if type(node) is ir.SelfFunction:
            self.cache[node.id] = res

        if isinstance(node, ir.MemberFunctionDef):
            self.cache[node.name] = res

        return res

    def generic_visit(self, node):
        r = False
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                t = reduce(lambda x, y: x or self.traverse(y), value, False)

            elif isinstance(value, ast.AST):
                t = self.visit(value)
            else: # If the field is a string or integer etc. then False
                t = False
            r = r or t
        return r


    def traverse(self, node):
        if type(node) is list:
            return reduce(lambda x, y : x or self.traverse(y), node, False)
        else:
            return self.visit(node)

    def visit_Module(self, node):
        return self.traverse(node.classes)

    def visit_ClassDef(self, node):
        self.class_table = self.table[node.name]
        r = self.traverse(node.functions)
        self.class_table = None
        return r

    def visit_MemberFunctionDef(self, node):

        return self.traverse(node.body)

    def visit_SelfFunction(self, node):
        t = self.class_table[node.id]

        # The following line currently fails as 't' is a list, since the lookup to class_table returns a list of suitable functions, not
        # the exact function. The only way to know which exact function is called is via the _Deduction class. Maybe the solution
        # Is to include type information in all ir nodes?
        return self.traverse(t.ast_node)

    def visit_Reassign(self, node):
        if type(node.target) is ir.SelfVariable:
            return True

        return False
