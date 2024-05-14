
# The following classes represent all the 'types' that Mylang objects can be

class MType:
    def mangle(self) -> str:
        pass

class Boolean(MType):

    def mangle(self):
        return "b"

    def __repr__(self):
        return "Boolean"


class Integer(MType):

    def mangle(self):
        return "i"

    def __repr__(self):
        return "Integer"


class Char(MType):

    def mangle(self):
        return "c"

    def __repr__(self):
        return "Char"


class Floating(MType):
    def mangle(self):
        return "f"

    def __repr__(self):
        return "Float"


class ID(MType):
    def mangle(self):
        return "a"

    def __repr__(self):
        return "ID"


class Vector(MType):
    def __init__(self, element_type: MType):
        self.element_type = element_type

    def mangle(self):
        return "l" + self.element_type.mangle()

    def __repr__(self):
        return "Vector(" + repr(self.element_type) + ")"


class String(MType):
    def mangle(self):
        return "u"

    def __repr__(self):
        return "String"


class Bytes(MType):
    def mangle(self):
        return "m"

    def __repr__(self):
        return "Bytes"


class Dictionary(MType):
    def __init__(self, key_type: MType, value_type: MType):
        self.key_type = key_type
        self.value_type = value_type

    def mangle(self):
        return "d" + self.key_type.mangle() + self.value_type.mangle()


    def __repr__(self):
        return "Dict(" + repr(self.key_type) + ", " + repr(self.value_type) + ")"


class DynamicSet(MType):
    def __init__(self, element_type: MType):
        self.element_type = element_type

    def mangle(self):
        return "s" + self.element_type.mangle()


    def __repr__(self):
        return "Set(" + repr(self.element_type) + ")"


class Option(MType):
    def __init__(self, contained_type: MType):
        self.contained_type = contained_type

    def mangle(self):
        return "o" + self.contained_type.mangle()


    def __repr__(self):
        return "Option(" + repr(self.contained_type) + ")"


class Result(MType):
    def __init__(self, ok_type: MType, err_type: MType):
        self.ok_type = ok_type
        self.err_type = err_type

    def mangle(self):
        return "r" + self.ok_type.mangle() + self.err_type.mangle()

    def __repr__(self):
        return "Result(" + repr(self.ok_type) + ", " + repr(self.err_type) + ")"

#class UserClass:
#    def __init__(self, identifier):
#        self.identifier = identifier
