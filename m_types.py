from collections import OrderedDict

# The following classes represent all the 'types' that Mylang objects can be

class MType:
    def mangle(self) -> str:
        pass

    def __hash__(self):
        return hash(self.mangle())

    def __eq__(self, other):
        return self.mangle() == other.mangle()

    def __next__(self, other):
        return not self == other

    def get_type(self):
        return self


# Convenience function. Used when the type is not immediately know, for example when declaring an empty array the
# type would be Vector(Unknown)
class Unknown:
    def __init__(self, inner=None):
        self.inner = inner

    def __repr__(self):
        return f"Unknown({self.inner})"

    def fill(self, inner):
        self.inner = inner

    def mangle(self):
        return self.inner.mangle()

    def __eq__(self, other):
        assert self.inner and other.inner
        return self.inner == other.inner

    def __hash__(self):
        return hash(id(self))

    def get_type(self):
        if self.inner:
            return self.inner
        else:
            return "Cannot unwrap Unkown with uninitialised type"


class Boolean(MType):

    _fields = []

    def mangle(self):
        return "b"

    def __repr__(self):
        return "Boolean"


class Integer(MType):

    _fields = []

    def mangle(self):
        return "i"

    def __repr__(self):
        return "Integer"


class Char(MType):

    _fields = []

    def mangle(self):
        return "c"

    def __repr__(self):
        return "Char"


class Floating(MType):

    _fields = []
    def mangle(self):
        return "f"

    def __repr__(self):
        return "Float"


class ID(MType):

    _fields = []
    def mangle(self):
        return "a"

    def __repr__(self):
        return "ID"


class Ntuple(MType):

    _fields = ["tuple_types"]

    def __init__(self, tuple_types):
        self.tuple_types = tuple_types

    def mangle(self):
        return "t" + str(len(self.tuple_types)) + "".join(map(lambda x : x.mangle(), self.tuple_types))

    def __repr__(self):
        return f"Tuple({self.tuple_types})"


class Vector(MType):

    _fields = ["element_type"]

    def __init__(self, element_type: MType):
        self.element_type = element_type

    def mangle(self):
        return "l" + self.element_type.mangle()

    def __repr__(self):
        return "Vector(" + repr(self.element_type) + ")"

    def get_type(self):
        return Vector(self.element_type.get_type())


class String(MType):

    _fields = []

    def mangle(self):
        return "u"

    def __repr__(self):
        return "String"


class Bytes(MType):

    _fields = []

    def mangle(self):
        return "m"

    def __repr__(self):
        return "Bytes"


class Dictionary(MType):

    _fields = ["key_type", "value_type"]

    def __init__(self, key_type: MType, value_type: MType):
        self.key_type = key_type
        self.value_type = value_type

    def mangle(self):
        return "d" + self.key_type.mangle() + self.value_type.mangle()


    def __repr__(self):
        return "Dictionary(" + repr(self.key_type) + ", " + repr(self.value_type) + ")"

    def get_type(self):
        return Dictionary(self.key_type.get_type(), self.value_type.get_type())


class DynamicSet(MType):

    _fields = ["element_type"]

    def __init__(self, element_type: MType):
        self.element_type = element_type

    def mangle(self):
        return "s" + self.element_type.mangle()

    def __repr__(self):
        return "Set(" + repr(self.element_type) + ")"

    def get_type(self):
        return DynamicSet(self.element_type.get_type())


class Option(MType):

    _fields = ["contained_type"]

    def __init__(self, contained_type: MType):
        self.contained_type = contained_type

    def mangle(self):
        return "o" + self.contained_type.mangle()


    def __repr__(self):
        return "Option(" + repr(self.contained_type) + ")"

    def get_type(self):
        return Option(self.contained_type.get_type())


class Result(MType):

    _fields = ["ok_type", "err_type"]

    def __init__(self, ok_type: MType, err_type: MType):
        self.ok_type = ok_type
        self.err_type = err_type

    def mangle(self):
        return "r" + self.ok_type.mangle() + self.err_type.mangle()

    def __repr__(self):
        return "Result(" + repr(self.ok_type) + ", " + repr(self.err_type) + ")"

    def get_type(self):
        return Result(self.ok_type.get_type(), self.err_type.get_type())


# Used when no annotation is provided for a type, and can match any type
class WildCard:

    _fields = []

    def __repr__(self):
        return "WildCard"


# Represents a code-generated user class complete with mangled name and dictionary of variable names to types
class UserClass(MType):
    def __init__(self, identifier, member_types):
        self.identifier = identifier
        self.member_types = member_types

    def __repr__(self):
        return f"Class('{self.identifier}', {repr(self.member_types)})"


    def mangle(self):
        import mangler

        mang = mangler.Name(self.identifier).mangle()

        for field in self.member_types.values():
            mang = mang + field.mangle()

        return "C" + str(len(mang)) + mang
