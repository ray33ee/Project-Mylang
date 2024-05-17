# This module contains classes which together define an intermediate representation created by the translator from
# mylang source and is itself converted into rust source code.


class Expression:
    pass


class SolitarySelf(Expression):
    pass

class Constant(Expression):
    def __init__(self, value):
        self.value = value

class MemberFunction(Expression):
    def __init__(self, expr: Expression, id: str, args: list[Expression]):
        self.expr = expr
        self.id = id
        self.args = args


class ClassConstructor(Expression):
    def __init__(self, class_name: str, args: list[Expression]):
        self.class_name = class_name
        self.args = args


class Statement:
    pass


class IfElse(Statement):
    def __init__(self, if_block: list[Statement], else_block: list[Statement] = None):
        self.if_block = if_block
        self.else_block = else_block


class Return(Statement):
    def __init__(self, expr: Expression):
        self.expr = expr


class LetAssign(Statement):
    pass


class Reassign(Statement):
    pass

class Function:
    def __init__(self, name):
        self.name = name
        self.body = []
        self.ret_type = None

    def add_statement(self, statement: Statement):
        self.body.append(statement)

    def set_return_type(self, ret_type):
        self.ret_type = ret_type

    def __repr__(self):
        return f"Function(name='{self.name}', body={self.body})"


class Class:
    def __init__(self, name, member_map):
        self.name = name
        self.member_map = member_map
        self.functions = {}

    def add_function(self, function: Function):
        self.functions[function.name] = function

    def __repr__(self):
        return f"Class('{self.name}', {self.member_map}, {repr(self.functions)})"

class Module:
    def __init__(self):
        self.functions = {}
        self.classes = {}

    def add_function(self, function: Function):
        if function.name not in self.functions:
            self.functions[function.name] = function

    def add_class(self, cl: Class):
        if cl.name not in self.classes:
            self.classes[cl.name] = cl

    def add_member_function(self, class_name, function: Function):

        self.classes[class_name].add_function(function)

    def get_class(self, name):
        return self.classes[name]

    def rustify(self, level=0, indent=4):
        pass

    def __repr__(self):
        return f"Module(functions={repr(self.functions)}, classes={repr(self.classes)})"




