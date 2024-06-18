
import logging
import m_types

logger = logging.getLogger(__name__)


class MemberVariable:
    def __init__(self, id):
        self.id = id

def mangle(thing):
    m = _Mangle()
    m.visit(thing)
    return _Mangle.MANGLE_STARTER + "".join(m.mangle)

class _Mangle:

    # All identifiers used by the mangler, sorted by case and then alphabetically

    MANGLE_STARTER = "_Z"

    CLASS = "C"
    NAME_END = "E"
    FUNCTION = "F"
    NAME_START = "N"
    VARIABLE = "V"

    ID_TYPE = "a"
    BOOLEAN_TYPE = "b"
    CHAR_TYPE = "c"
    DICTIONARY_TYPE = "d"
    FLOATING_TYPE = "f"
    INTEGER_TYPE = "i"
    POSITIVE_INTEGER = "j"
    NEGATIVE_INTEGER = "k"
    VECTOR_TYPE = "l"
    BYTES_TYPE = "m"
    OPTION_TYPE = "o"
    RESULT_TYPE = "r"
    SET_TYPE = "s"
    TUPLE_TYPE = "t"
    STRING_TYPE = "u"

    def __init__(self):
        self.mangle = []

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method)
        return visitor(node)

    def write(self, text):
        if type(text) is str:
            self.mangle.append(text)
        elif type(text) is list:
            for t in text:
                self.write(t)
        else:
            raise "Write function only works on strings or list of strings"

    # Prepends a string s with its length
    def length(self, s):
        self.write(str(len(s)))
        self.write(s)

    def generic_name(self, name):
        self.write(self.NAME_START)
        if type(name) is list:
            for n in name:
                self.length(n)
        else:
            self.length(name)
        self.write(self.NAME_END)

    # Write an integer value, distinguishing between positive and negatives
    def generic_integer(self, num):
        if num > 0:
            self.write(self.POSITIVE_INTEGER)
        else:
            self.write(self.NEGATIVE_INTEGER)
        f = format(abs(num), 'x')
        self.write(f)

    def generic_types(self, name, types):
        m = _Mangle()
        m.generic_name(name)
        for t in types:
            m.visit(t)
        s = "".join(m.mangle)
        self.length(s)

    def generic_variable(self, name, unique):
        self.write(self.VARIABLE)
        self.generic_name(name)
        self.generic_integer(unique)

    def generic_function(self, name, arg_types):
        self.write(self.FUNCTION)
        self.generic_types(name, arg_types)

    def generic_class(self, name, member_types):
        self.write(self.CLASS)
        self.generic_types(name, member_types)

    def visit_Arg(self, node):
        self.visit(node.annotation)

    def visit_Member(self, node):
        self.visit(node.annotation)

    def visit_Unknown(self, node):
        if node.has_inner():
            self.visit(node.inner())
        else:
            raise "Cannot call visit on unresolved unknown"

    def visit_Boolean(self, node):
        self.write(self.BOOLEAN_TYPE)

    def visit_Integer(self, node):
        self.write(self.INTEGER_TYPE)

    def visit_Char(self, node):
        self.write(self.CHAR_TYPE)

    def visit_Floating(self, node):
        self.write(self.FLOATING_TYPE)

    def visit_ID(self, node):
        self.write(self.ID_TYPE)

    def visit_Ntuple(self, node):
        self.write(self.TUPLE_TYPE)
        m = _Mangle()
        for e in node.tuple_types:
            m.visit(e)
        s = "".join(m.mangle)
        self.length(s)

    def visit_Vector(self, node):
        self.write(self.VECTOR_TYPE)
        self.visit(node.element_type)

    def visit_String(self, node):
        self.write(self.STRING_TYPE)

    def visit_Bytes(self, node):
        self.write(self.BYTES_TYPE)

    def visit_Dictionary(self, node):
        self.write(self.DICTIONARY_TYPE)
        self.visit(node.key_type)
        self.visit(node.value_type)

    def visit_DynamicSet(self, node):
        self.write(self.SET_TYPE)
        self.visit(node.element_type)

    def visit_Option(self, node):
        self.write(self.OPTION_TYPE)
        self.visit(node.contained_type)

    def visit_Result(self, node):
        self.write(self.RESULT_TYPE)
        self.visit(node.ok_type)
        self.visit(node.err_type)

    def visit_UserClass(self, node):
        self.generic_class(node.identifier, node.member_types)

    def visit_FunctionCall(self, node):
        self.generic_function(node.id, node.types)

    def visit_GlobalFunctionCall(self, node):
        self.generic_function(node.id, node.types)

    def visit_MemberFunction(self, node):
        self.generic_function(node.id, node.types)

    def visit_SelfFunction(self, node):
        self.generic_function(node.id, node.types)

    def generic_functiondef(self, node):
        self.generic_function(node.name, node.args)

    def visit_FunctionDef(self, node):
        self.generic_functiondef(node)

    def visit_MainFunctionDef(self, node):
        self.generic_functiondef(node)

    def visit_MemberFunctionDef(self, node):
        self.generic_functiondef(node)

    def visit_InitFunctionDef(self, node):
        self.generic_functiondef(node)

    def visit_ClassDef(self, node):
        self.generic_class(node.name, node.member_map)

    def visit_Assign(self, node):
        self.generic_variable(["tmp", "var", "mangled"], id(node))

    def generic_memberassign(self, id):
        # Here we use a 'unique' value of 0 because the name [self, node.id] is enough to guarantee uniqueness
        self.generic_variable(["self", id], 0)

    def visit_InitAssign(self, node):
        self.generic_memberassign(node.id)

    def visit_MemberVariable(self, node):
        self.generic_memberassign(node.id)

    def visit_TestFunction(self, node):
        self.generic_function(node.name, node.args)

    def visit_TestClass(self, node):
        self.generic_class(node.name, node.members)


class TestFunction:

    def __init__(self, name, args):
        self.name = name
        self.args = args


class TestClass:
    def __init__(self, name, members):
        self.name = name
        self.members = members


def mangler_test_function(obj, verbose=False):

    if type(obj) is list:
        s = set()

        for o in obj:
            s.add(mangler_test_function(o, verbose))

        # Make sure that every distinct test creates a distinct mangled string
        return len(s)
    else:
        mangled = mangle(obj)

        if verbose:
            logger.debug("Body:      " + repr(obj))
            logger.debug("Mangled:   " + str(mangled))

        return mangled


def run_mangler_tests(verbose=False):
    import ir
    from collections import OrderedDict

    # Here we create a bunch of very different and very similar symbols. They are all distinct, so their mangled
    # names should be different
    bank1 = [
        # Same name, same arg types, different number of args
        TestFunction("test1", []),
        TestFunction("test1", [m_types.Integer()]),
        TestFunction("test1", [m_types.Integer(), m_types.Integer()]),

        # Same name, same number of args, different types
        TestFunction("test2", [m_types.Integer()]),
        TestFunction("test2", [m_types.Floating()]),
        TestFunction("test2", [m_types.Char()]),

        TestFunction("test3", [m_types.Integer(), m_types.Integer()]),

        # Same name, same number of fields different field types
        ir.ClassDef("complex", [m_types.Floating(), m_types.Floating()]),
        ir.ClassDef("complex", [m_types.Integer(), m_types.Integer()]),

        ir.ClassDef("complex", [m_types.Integer()]),
        ir.ClassDef("complex", [m_types.Bytes()]),

        # Make sure that none of the built in types clash
        TestFunction("t", [m_types.Boolean()]),
        TestFunction("t", [m_types.Integer()]),
        TestFunction("t", [m_types.Char()]),
        TestFunction("t", [m_types.Floating()]),
        TestFunction("t", [m_types.ID()]),
        TestFunction("t", [m_types.String()]),
        TestFunction("t", [m_types.Bytes()]),

        TestFunction("t", [m_types.Vector(m_types.Integer())]),
        TestFunction("t", [m_types.Vector(m_types.Floating())]),
        TestFunction("t", [m_types.Vector(m_types.Vector(m_types.Vector(m_types.Vector(m_types.Floating()))))]),

        TestFunction("t", [m_types.Option(m_types.Integer())]),
        TestFunction("t", [m_types.Option(m_types.String())]),

    ]

    if mangler_test_function(bank1, verbose) != len(bank1):
        logger.warning("Bank 1 of mangler tests failed")
        raise "bank 1 failed"

    # Here we copy the same symbol over and over many times. This should collapse to one mangled string
    # as they are all the same. THis test is important to make sure that the order of symbols in class fields and
    # function arguments is preserved
    bank2 = [

        TestFunction("test4", [m_types.Bytes(), m_types.ID()]),
        TestFunction("test4", [m_types.Bytes(), m_types.ID()]),
        TestFunction("test4", [m_types.Bytes(), m_types.ID()]),
        TestFunction("test4", [m_types.Bytes(), m_types.ID()]),
        TestFunction("test4", [m_types.Bytes(), m_types.ID()]),
        TestFunction("test4", [m_types.Bytes(), m_types.ID()]),
        TestFunction("test4", [m_types.Bytes(), m_types.ID()]),
        TestFunction("test4", [m_types.Bytes(), m_types.ID()]),
        TestFunction("test4", [m_types.Bytes(), m_types.ID()]),
        TestFunction("test4", [m_types.Bytes(), m_types.ID()]),

    ]

    if mangler_test_function(bank2, verbose) != 1:
        logger.warning("Bank 2 of mangler tests failed")
        raise "bank 2 failed"

    bank3 = [

        TestFunction("test5", [m_types.Ntuple([])]),
        TestFunction("test5", [m_types.Ntuple([]), m_types.Ntuple([])]),
        TestFunction("test5", [m_types.Ntuple([m_types.Bytes()])]),
        TestFunction("test5", [m_types.Ntuple([m_types.Floating()])]),
        TestFunction("test5", [m_types.Ntuple([m_types.Bytes(), m_types.String()])]),

        TestFunction("test5", [m_types.Ntuple([m_types.Bytes()]), m_types.Ntuple([m_types.String()])]),
        TestFunction("test5", [m_types.Ntuple([m_types.Bytes(), m_types.Ntuple([m_types.String()])])]),

    ]

    if mangler_test_function(bank3, verbose) != len(bank3):
        logger.warning("Bank 3 of mangler tests failed")
        raise "bank 3 failed"

    logger.debug("All tests passed")



