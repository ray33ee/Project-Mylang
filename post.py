import ast

import ir


def post_processing(_ir: ir.Module):
    p = _Post()

    return p.visit(_ir)


class _Post(ast.NodeTransformer):

    def __init__(self):
        pass

    def visit_ClassDef(self, node):
        return ir.CyclicClassDef(node)

