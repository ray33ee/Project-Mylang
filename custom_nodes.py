import ast

# A Self on its own, without accessing any attributes (for example return self, or x = self)
class SolitarySelf(ast.AST):

    _fields = ()
    def __init__(self):
        super().__init__()


# A Self.SOMETHING, a special type of attribute
class SelfMemberVariable(ast.AST):

    _fields = ["id"]
    def __init__(self, identifier):
        super().__init__()
        self.id = identifier

class SelfMemberFunction(ast.AST):

    _fields = ["id", "args"]
    def __init__(self, identifier, args):
        super().__init__()
        self.id = identifier
        self.args = args



# expression.identifier(args), member function call
class MemberFunction(ast.AST):

    _fields = ["expr", "id", "args"]
    def __init__(self, expr: ast.expr, identifier, args):
        super().__init__()
        self.expr = expr
        self.id = identifier
        self.args = args


# expression.identifier(args), member function call
class MemberVariable(ast.AST):

    _fields = ["expr", "id"]
    def __init__(self, expr: ast.expr, identifier):
        super().__init__()
        self.expr = expr
        self.id = identifier

class MyCall(ast.AST):

    _fields = ["id", "args"]
    def __init__(self, identifier, args):
        super().__init__()
        self.id = identifier # ast.Name(identifier, ast.Load())
        self.args = args


