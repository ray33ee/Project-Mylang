import ast

# Reimplements ast's _Unparser to work with our custom AST nodes

class _Unparser(ast._Unparser):
    def __init__(self,  _avoid_backslashes=False):
        super().__init__()

    def visit_SolitarySelf(self, node):
        self.write("SOLITARYself")

    def visit_SelfMemberFunction(self, node):
        self.write("self.")
        self.write(node.id)
        with self.delimit("(", ")"):
            comma = False
            for a in node.args:
                if comma:
                    self.write(", ")
                else:
                    comma = True
                self.traverse(a)
    def visit_SelfMemberVariable(self, node):
        self.write("self.")
        self.write(node.id)

    def visit_MemberFunction(self, node):
        self.traverse(node.exp)
        self.write(".")
        self.write(node.id)
        with self.delimit("(", ")"):
            comma = False
            for a in node.args:
                if comma:
                    self.write(", ")
                else:
                    comma = True
                self.traverse(a)

    def visit_MyCall(self, node):
        self.write(node.id)
        with self.delimit("(", ")"):
            comma = False
            for a in node.args:
                if comma:
                    self.write(", ")
                else:
                    comma = True
                self.traverse(a)

    def visit_MonoAssign(self, node):
        self.fill()
        self.traverse(node.target)
        self.write(" = ")
        self.traverse(node.value)

def unparse(ast_obj):
    unparser = _Unparser()
    return unparser.visit(ast_obj)