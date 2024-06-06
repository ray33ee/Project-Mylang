import ast

import m_types
import mangler

from collections import OrderedDict


# This module contains classes which together define an intermediate representation created by the translator from
# mylang source and is itself converted into rust source code.


class Expression(ast.AST):
    pass


class GlobalFunctionCall(Expression):

    _fields = ["id", "args"]

    def __init__(self, _id, args):
        super().__init__()
        self.id = _id
        self.args = args


class SolitarySelf(Expression):
    pass

class Constant(Expression):

    _fields = ["value"]

    def __init__(self, value):
        super().__init__()
        self.value = value


class MemberFunction(Expression):

    _fields = ["expr", "id", "args"]

    def __init__(self, expr: Expression, _id: str, args: list[Expression]):
        super().__init__()
        self.expr = expr
        self.id = _id
        self.args = args

class SelfFunction(Expression):

    _fields = ["id", "args"]

    def __init__(self, _id: str, args: list[Expression]):
        super().__init__()
        self.id = _id
        self.args = args

class SelfVariable(Expression):

    _fields = ["id"]

    def __init__(self, _id: str):
        super().__init__()
        self.id = _id


class ClassConstructor(Expression):

    _fields = ["class_name", "args"]

    def __init__(self, class_name: str, args: list[Expression]):
        super().__init__()
        self.class_name = class_name
        self.args = args


class Identifier(Expression):

    _fields = ["id"]

    def __init__(self, _id):
        super().__init__()
        self.id = _id

class IRTuple(Expression):

    _fields = ["elements"]

    def __init__(self, elements):
        super().__init__()
        self.elements = elements

class Statement(ast.AST):
    pass


class IfElse(Statement):

    _fields = ["if_block", "else_block"]

    def __init__(self, if_block: list[Statement], else_block: list[Statement] = None):
        super().__init__()
        self.if_block = if_block
        self.else_block = else_block


class Return(Statement):

    _fields = ["expr"]

    def __init__(self, expr: Expression):
        super().__init__()
        self.expr = expr


class LetAssign(Statement):
    pass


class Reassign(Statement):
    pass

class FunctionDef(ast.AST):

    _fields = ["name", "body", "ret_type", "args"]

    def __init__(self, name, args):
        super().__init__()
        self.name = name
        self.body = []
        self.ret_type = None

        # Must be an ordered dict mapping arg names to arg types
        assert type(args) is OrderedDict
        self.args = args

    def add_statement(self, statement: Statement):
        self.body.append(statement)

    def set_return_type(self, ret_type):
        self.ret_type = ret_type

    def __repr__(self):
        return f"Function(name='{self.name}', args={self.args}, body={self.body})"

    def mangle(self):
        mang = mangler.Name(self.name).mangle()

        for a in self.args.values():
            mang = mang + a.mangle()

        return "F" + str(len(mang)) + mang


class ClassDef(ast.AST):

    _fields = ["name", "member_map", "functions"]

    def __init__(self, name, member_map):
        super().__init__()
        self.name = name

        # Must be an ordered dict mapping agr names to types
        self.member_map = member_map
        self.functions = []

    def add_function(self, function: FunctionDef):
        self.functions.append(function)

    def __repr__(self):
        return f"Class('{self.name}', {self.member_map}, {repr(self.functions)})"

    def mangle(self):
        # Here we leverage the UserClass mangling to do our work for us
        return m_types.UserClass(self.name, self.member_map).mangle()



class Module(ast.AST):

    _fields = ["functions", "classes"]

    def __init__(self):
        super().__init__()
        self.functions = []
        self.classes = []

    def add_function(self, function: FunctionDef):
        self.functions.append(function)

    def add_class(self, cl: ClassDef):
        self.classes.append(cl)

    def __repr__(self):
        return f"Module(functions={repr(self.functions)}, classes={repr(self.classes)})"




