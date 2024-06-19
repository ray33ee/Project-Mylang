import ast

import m_types

from collections import OrderedDict


# This module contains classes which together define an intermediate representation created by the translator from
# mylang source and is itself converted into rust source code.


class Arg(ast.AST):

    _fields = ["id", "annotation"]

    def __init__(self, id, annotation):
        super().__init__()
        self.id = id
        self.annotation = annotation


class Member(ast.AST):

    _fields = ["id", "annotation"]

    def __init__(self, id, annotation):
        super().__init__()
        self.id = id
        self.annotation = annotation


class Expression(ast.AST):
    pass


class FunctionCall(Expression):


    pass


class GlobalFunctionCall(FunctionCall):

    _fields = ["id", "args", "types"]

    def __init__(self, _id, args, types):
        super().__init__()
        self.id = _id
        self.args = args
        self.types = types


class SolitarySelf(Expression):
    pass


class List(Expression):

    _fields = ["elements"]

    def __init__(self, elements):
        super().__init__()
        self.elements = elements


class Tuple(Expression):

    _fields = ["elements"]

    def __init__(self, elements):
        super().__init__()
        self.elements = elements

class Constant(Expression):

    _fields = ["value"]

    def __init__(self, value):
        super().__init__()
        self.value = value


class BuiltInMemberFunction(FunctionCall):

    _fields = ["expr", "id", "args", "types"]

    def __init__(self, expr: Expression, _id: str, args: list[Expression], types):
        super().__init__()
        self.expr = expr
        self.id = _id
        self.args = args
        self.types = types


class UserClassMemberFunction(FunctionCall):

    _fields = ["expr", "id", "args", "types"]

    def __init__(self, expr: Expression, _id: str, args: list[Expression], types):
        super().__init__()
        self.expr = expr
        self.id = _id
        self.args = args
        self.types = types


class SelfFunction(FunctionCall):

    _fields = ["id", "args"]

    def __init__(self, _id: str, args: list[Expression], types):
        super().__init__()
        self.id = _id
        self.args = args
        self.types = types

class SelfVariable(Expression):

    _fields = ["id"]

    def __init__(self, _id: str):
        super().__init__()
        self.id = _id


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


class ClassConstructor(Expression):

    _fields = ["usr_class", "args"]

    def __init__(self, usr_class: m_types.UserClass, args, types):
        super().__init__()
        self.usr_class = usr_class
        self.args = args
        self.types = types

class Statement(ast.AST):
    pass


class Expr(Statement):

    _fields = ["expr"]

    def __init__(self, expr):
        super().__init__()
        self.expr = expr

class IfElse(Statement):

    _fields = ["condition", "if_block", "else_block"]

    def __init__(self, condition, if_block: list[Statement], else_block: list[Statement] = None):
        super().__init__()
        self.condition = condition
        self.if_block = if_block
        self.else_block = else_block

class While(Statement):

    _fields = ["condition", "body"]

    def __init__(self, condition, body: list[Statement]):
        super().__init__()
        self.condition = condition
        self.body = body

class For(Statement):

    _fields = ["target", "iterator", "body"]

    def __init__(self, target, iterator, body: list[Statement]):
        super().__init__()
        self.target = target
        self.iterator = iterator
        self.body = body


class Return(Statement):

    _fields = ["expr"]

    def __init__(self, expr: Expression):
        super().__init__()
        self.expr = expr


class LetAssign(Statement):

    _fields = ["target", "value"]

    def __init__(self, target, value):
        super().__init__()
        self.target = target
        self.value = value


class Reassign(Statement):

    _fields = ["target", "value"]

    def __init__(self, target, value):
        super().__init__()
        self.target = target
        self.value = value


class Break(ast.AST):
    pass


class Continue(ast.AST):
    pass


class FunctionDef(ast.AST):

    _fields = ["name", "args", "ret_type", "body"]

    def __init__(self, name, args):
        super().__init__()
        self.name = name
        self.body = []
        self.ret_type = m_types.Ntuple([])

        self.args = args

    def add_statement(self, statement: Statement):
        self.body.append(statement)

    def set_return_type(self, ret_type):
        self.ret_type = ret_type

    def __repr__(self):
        return f"Function(name='{self.name}', args={self.args}, body={self.body})"



class MainFunctionDef(FunctionDef):

    def __init__(self, ir_func: FunctionDef):
        super().__init__("main", [])
        self.body = ir_func.body
        self.ret_type = ir_func.ret_type


class MemberFunctionDef(FunctionDef):

    def __init__(self, ir_func: FunctionDef):
        super().__init__(ir_func.name, ir_func.args)
        self.body = ir_func.body
        self.ret_type = ir_func.ret_type



class InitFunctionDef(FunctionDef):
    def __init__(self, name, args, member_list):
        super().__init__(name, args)
        self.member_list = member_list


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


# Represents a class that exists on the heap with cyclic reference counting
class CyclicClassDef(ClassDef):

    def __init__(self, classdef):
        super().__init__(classdef.name, classdef.member_map)
        self.functions = classdef.functions


# Represents a class that exists on the heap with standard reference counting
class AcyclicClassDef(ClassDef):

    def __init__(self, classdef):
        super().__init__(classdef.name, classdef.member_map)
        self.functions = classdef.functions


# Represents a class that exists on the stack
class StackClassDef(ClassDef):

    def __init__(self, classdef):
        super().__init__(classdef.name, classdef.member_map)
        self.functions = classdef.functions


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




