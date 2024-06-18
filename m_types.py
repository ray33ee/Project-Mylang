from collections import OrderedDict
import ast

import mangle


# The following classes represent all the 'types' that Mylang objects can be

class MType(ast.AST):
    def __hash__(self):
        return hash(mangle.mangle(self))

    def __eq__(self, other):
        return mangle.mangle(self) == mangle.mangle(other)

    def get_type(self):
        return self


# Convenience function. Used when the type is not immediately know, for example when declaring an empty array the
# type would be Vector(Unknown)
class Unknown:

    class Dependant:
        def __init__(self, unknown, node, arg_types):
            self.unknown = unknown
            self.node = node
            self.arg_types = arg_types

    def __init__(self, deductor, inner=None):
        self._inner = inner
        self.deductor = deductor
        self._depends = []

    def fill(self, inner):
        import deduction

        # Resolve this unknown
        self._inner = inner

        # Resolve any unknowns linked to self
        for dependant in self._depends:
            t = self.deductor.handle_builtin(dependant.node, inner, dependant.arg_types)
            dependant.unknown.fill(t)

    def add_dependent(self, unknown, node, arg_types):
        self._depends.append(self.Dependant(unknown, node, arg_types))

    def __eq__(self, other):
        assert self._inner and other._inner
        return self._inner == other._inner

    def __hash__(self):
        return hash(id(self))

    def has_inner(self):
        return self._inner is not None

    def inner(self):
        return self._inner

    def __repr__(self):
        if self._inner:
            return f"Unknown({ast.dump(self._inner)})"
        else:
            return "Unknown()"

    def get_type(self):
        if self._inner:
            return self._inner
        else:
            raise "Cannot unwrap Unknown with uninitialised type"




class Boolean(MType):

    _fields = []


class Integer(MType):

    _fields = []


class Char(MType):

    _fields = []


class Floating(MType):

    _fields = []


class ID(MType):

    _fields = []


class Ntuple(MType):

    _fields = ["tuple_types"]

    def __init__(self, tuple_types):
        self.tuple_types = tuple_types


class Vector(MType):

    _fields = ["element_type"]

    def __init__(self, element_type: MType):
        self.element_type = element_type

    def get_type(self):
        return Vector(self.element_type.get_type())


class String(MType):

    _fields = []


class Bytes(MType):

    _fields = []


class Dictionary(MType):

    _fields = ["key_type", "value_type"]

    def __init__(self, key_type: MType, value_type: MType):
        self.key_type = key_type
        self.value_type = value_type

    def get_type(self):
        return Dictionary(self.key_type.get_type(), self.value_type.get_type())


class DynamicSet(MType):

    _fields = ["element_type"]

    def __init__(self, element_type: MType):
        self.element_type = element_type

    def get_type(self):
        return DynamicSet(self.element_type.get_type())


class Option(MType):

    _fields = ["contained_type"]

    def __init__(self, contained_type: MType):
        self.contained_type = contained_type

    def get_type(self):
        return Option(self.contained_type.get_type())


class Result(MType):

    _fields = ["ok_type", "err_type"]

    def __init__(self, ok_type: MType, err_type: MType):
        self.ok_type = ok_type
        self.err_type = err_type

    def get_type(self):
        return Result(self.ok_type.get_type(), self.err_type.get_type())


# Used when no annotation is provided for a type, and can match any type
class WildCard(MType):

    _fields = []


# Represents a code-generated user class complete with mangled name and dictionary of variable names to types
class UserClass(MType):

    _fields = ["identifier", "member_types"]

    def __init__(self, identifier, member_types):
        self.identifier = identifier
        self.member_types = member_types

