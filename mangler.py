import m_types

# Describes an identifier, such as the name of a function or class.
# Constructed of a set of strings which represent namespaces, modules, any kind of scoped access
class Name:
    def __init__(self, names):
        if type(names) is str:
            self.names = [names]
        elif type(names) is list:
            self.names = names

    def mangle(self):
        s = "N"

        for name in self.names:
            s = s + str(len(name)) + name

        return s + "E"

    def __repr__(self):
        s = self.names[0]

        for i in range(len(self.names) - 1):
            s = s + "." + self.names[i+1]

        return s


class Mangle:
    def __init__(self, obj):
        self.mangled_string = "_Z" + obj.mangle()

    def __hash__(self):
        return hash(self.mangled_string)

    def __eq__(self, other: str):
        return self.mangled_string == other

    def __str__(self):
        return str(self.mangled_string)

    def __repr__(self):
        return repr(self.mangled_string)


def mangler_test_function(obj, verbose=False):

    if type(obj) is list:
        s = set()

        for o in obj:
            s.add(mangler_test_function(o, verbose))

        # Make sure that every distinct test creates a distinct mangled string
        return len(s)
    else:
        mangled = Mangle(obj)

        if verbose:
            print("Body:      " + repr(obj))
            print("Mangled:   " + str(mangled))

        return mangled


def run_mangler_tests():
    import ir
    from collections import OrderedDict

    # Here we create a bunch of very different and very similar symbols. They are all distinct, so their mangled
    # names should be different
    bank1 = [
        # Same name, same arg types, different number of args
        ir.FunctionDef("test1", OrderedDict({})),
        ir.FunctionDef("test1", OrderedDict({"a": m_types.Integer()})),
        ir.FunctionDef("test1", OrderedDict({"a": m_types.Integer(), "b": m_types.Integer()})),

        # Same name, same number of args, different types
        ir.FunctionDef("test2", OrderedDict({"a": m_types.Integer()})),
        ir.FunctionDef("test2", OrderedDict({"a": m_types.Floating()})),
        ir.FunctionDef("test2", OrderedDict({"a": m_types.Char()})),

        ir.FunctionDef("test3", OrderedDict({"a": m_types.Integer(), "b": m_types.Integer()})),

        # Same name, same number of fields different field types
        ir.ClassDef("complex", OrderedDict({"real": m_types.Floating(), "imag": m_types.Floating()})),
        ir.ClassDef("complex", OrderedDict({"real": m_types.Integer(), "imag": m_types.Integer()})),

        ir.ClassDef("complex", OrderedDict({"real": m_types.Integer()})),
        ir.ClassDef("complex", OrderedDict({"real": m_types.Bytes()})),

        # Make sure that none of the built in types clash
        ir.FunctionDef("t", OrderedDict({"a": m_types.Boolean()})),
        ir.FunctionDef("t", OrderedDict({"a": m_types.Integer()})),
        ir.FunctionDef("t", OrderedDict({"a": m_types.Char()})),
        ir.FunctionDef("t", OrderedDict({"a": m_types.Floating()})),
        ir.FunctionDef("t", OrderedDict({"a": m_types.ID()})),
        ir.FunctionDef("t", OrderedDict({"a": m_types.String()})),
        ir.FunctionDef("t", OrderedDict({"a": m_types.Bytes()})),

        ir.FunctionDef("t", OrderedDict({"a": m_types.Vector(m_types.Integer())})),
        ir.FunctionDef("t", OrderedDict({"a": m_types.Vector(m_types.Floating())})),
        ir.FunctionDef("t", OrderedDict({"a": m_types.Vector(m_types.Vector(m_types.Vector(m_types.Vector(m_types.Floating()))))})),

        ir.FunctionDef("t", OrderedDict({"a": m_types.Option(m_types.Integer())})),
        ir.FunctionDef("t", OrderedDict({"a": m_types.Option(m_types.String())})),

    ]

    if mangler_test_function(bank1, True) != len(bank1):
        print("Bank 1 of mangler tests failed")
        raise "bank 1 failed"

    # Here we copy the same symbol over and over many times. This should collapse to one mangled string
    # as they are all the same. THis test is important to make sure that the order of symbols in class fields and
    # function arguments is preserved
    bank2 = [

        ir.FunctionDef("test4", OrderedDict({"a": m_types.Bytes(), "b": m_types.ID()})),
        ir.FunctionDef("test4", OrderedDict({"a": m_types.Bytes(), "b": m_types.ID()})),
        ir.FunctionDef("test4", OrderedDict({"a": m_types.Bytes(), "b": m_types.ID()})),
        ir.FunctionDef("test4", OrderedDict({"a": m_types.Bytes(), "b": m_types.ID()})),
        ir.FunctionDef("test4", OrderedDict({"a": m_types.Bytes(), "b": m_types.ID()})),
        ir.FunctionDef("test4", OrderedDict({"a": m_types.Bytes(), "b": m_types.ID()})),
        ir.FunctionDef("test4", OrderedDict({"a": m_types.Bytes(), "b": m_types.ID()})),
        ir.FunctionDef("test4", OrderedDict({"a": m_types.Bytes(), "b": m_types.ID()})),
        ir.FunctionDef("test4", OrderedDict({"a": m_types.Bytes(), "b": m_types.ID()})),
        ir.FunctionDef("test4", OrderedDict({"a": m_types.Bytes(), "b": m_types.ID()})),
        ir.FunctionDef("test4", OrderedDict({"a": m_types.Bytes(), "b": m_types.ID()})),

    ]

    if mangler_test_function(bank2, True) != 1:
        print("Bank 2 of mangler tests failed")
        raise "bank 2 failed"

    bank3 = [

        ir.FunctionDef("test5", OrderedDict({"a": m_types.Ntuple([])})),
        ir.FunctionDef("test5", OrderedDict({"a": m_types.Ntuple([]), "b": m_types.Ntuple([])})),
        ir.FunctionDef("test5", OrderedDict({"a": m_types.Ntuple([m_types.Bytes()])})),
        ir.FunctionDef("test5", OrderedDict({"a": m_types.Ntuple([m_types.Floating()])})),
        ir.FunctionDef("test5", OrderedDict({"a": m_types.Ntuple([m_types.Bytes(), m_types.String()])})),

        ir.FunctionDef("test5", OrderedDict({"a": m_types.Ntuple([m_types.Bytes()]), "b": m_types.Ntuple([m_types.String()])})),
        ir.FunctionDef("test5", OrderedDict({"a": m_types.Ntuple([m_types.Bytes(), m_types.Ntuple([m_types.String()])])})),

    ]

    if mangler_test_function(bank3, True) != len(bank3):
        print("Bank 3 of mangler tests failed")
        raise "bank 3 failed"

    print("All tests passed")

