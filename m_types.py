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
    def __init__(self, inner=None):
        self.inner = inner

    def fill(self, inner):
        self.inner = inner

    def __eq__(self, other):
        assert self.inner and other.inner
        return self.inner == other.inner

    def __hash__(self):
        return hash(id(self))

    def get_type(self):
        if self.inner:
            return self.inner
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

