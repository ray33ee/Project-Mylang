import ast

# Reimplements ast's _Unparser to work with our custom AST nodes

class _Unparser(ast._Unparser):
    def __init__(self,  _avoid_backslashes=False):
        super().__init__()

    def visit_SolitarySelf(self, node):
        self.write(node.id)

    def visit_SelfMemberVariable(self, node):
        self.visit_Attribute(node)

def unparse(ast_obj):
    unparser = _Unparser()
    return unparser.visit(ast_obj)