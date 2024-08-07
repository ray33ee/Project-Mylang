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

    def __init__(self, id, args, types=None):
        super().__init__()
        self.id = id
        self.args = args
        self.types = types


# expression.identifier(args), member function call
class MemberFunction(ast.AST):

    _fields = ["exp", "id", "args", "types", "exp_type"]

    def __init__(self, exp: ast.expr, id, args, types=None, exp_type=None):
        super().__init__()
        self.exp = exp
        self.id = id
        self.args = args
        self.types = types
        self.exp_type = exp_type



class MyCall(ast.AST):

    _fields = ["id", "args"]

    def __init__(self, id, args, types=None):
        super().__init__()
        self.id = id # ast.Name(identifier, ast.Load())
        self.args = args
        self.types = types


class ConstructorCall(ast.AST):

    _fields = ["class_id", "args"]

    def __init__(self, class_id, args, types=None):
        super().__init__()
        self.class_id = class_id
        self.args = args
        self.types = types


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

class GetterAssign(ast.AST):

    _fields = ["self_id", "value"]

    def __init__(self, self_id, value):
        super().__init__()
        self.self_id = self_id
        self.value = value


class InitAssign(ast.AST):

    _fields = ["id", "value"]

    def __init__(self, id, value):
        super().__init__()
        self.id = id
        self.value = value


class InitFunctionDef(ast.FunctionDef):

    _fields = ["args", "body"]

    def __init__(self, args, body, decorator_list, returns, type_comment, type_params):
        super().__init__()
        self.name = "__init__"
        self.args = args
        self.body = body
        self.member_list = None
        self.decorator_list = decorator_list
        self.returns = returns
        self.type_comment = type_comment
        self.type_params = type_params
        self.lineno = None


class DelFunctionDef(ast.FunctionDef):

    _fields = ["args", "body"]

    def __init__(self, body, decorator_list, returns, type_comment, type_params):
        super().__init__()
        self.name = "__del__"
        self.args = ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], defaults=[])
        self.body = body
        self.member_list = None
        self.decorator_list = decorator_list
        self.returns = returns
        self.type_comment = type_comment
        self.type_params = type_params
        self.lineno = None

class SomeCall(ast.AST):

    _fields = ["expr"]

    def __init__(self, expr):
        super().__init__()
        self.expr = expr

class BytesCall(ast.AST):

    _fields = []

    def __init__(self):
        super().__init__()


class BuiltInClassConstructor(ConstructorCall):


    def __init__(self, id, args, types=None):
        super().__init__(id, args, types)


class GetterFunctionDef(ast.FunctionDef):
    _fields = ["name", "body"]

    def __init__(self, name, body, decorator_list, returns, type_comment, type_params):
        super().__init__()
        self.name = name
        self.args = ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], defaults=[])
        self.body = body
        self.member_list = None
        self.decorator_list = decorator_list
        self.returns = returns
        self.type_comment = type_comment
        self.type_params = type_params
        self.lineno = None


class SetterFunctionDef(ast.FunctionDef):
    _fields = ["name", "args", "body"]

    def __init__(self, name, args, body, decorator_list, returns, type_comment, type_params):
        super().__init__()
        self.name = name
        self.args = args
        self.body = body
        self.member_list = None
        self.decorator_list = decorator_list
        self.returns = returns
        self.type_comment = type_comment
        self.type_params = type_params
        self.lineno = None