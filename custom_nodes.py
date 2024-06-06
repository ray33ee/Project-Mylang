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

    _fields = ["exp", "id", "args"]

    def __init__(self, exp: ast.expr, identifier, args):
        super().__init__()
        self.exp = exp
        self.id = identifier
        self.args = args


class MyCall(ast.AST):

    _fields = ["id", "args"]

    def __init__(self, identifier, args):
        super().__init__()
        self.id = identifier # ast.Name(identifier, ast.Load())
        self.args = args


# Declare and assign. maps to Rust's let statement
class MonoAssign(ast.AST):

    _fields = ["target", "value"]

    def __init__(self, target, value, assign_type=None):
        super().__init__()
        self.target = target
        self.value = value
        self.assign_type = assign_type


# Pure assign. Maps to a normal assignment without let
class Reassign(ast.AST):

    _fields = ["target", "value"]

    def __init__(self, target, value):
        super().__init__()
        self.target = target
        self.value = value