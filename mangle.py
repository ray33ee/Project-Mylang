
import ast

def mangle(thing):
    m = _Mangle()
    m.visit(thing)
    return "_Z" + "".join(m.mangle)

class _Mangle(ast.NodeVisitor):

    def __init__(self):
        self.mangle = []

    def write(self, text):
        if type(text) is str:
            self.mangle.append(text)
        elif type(text) is list:
            for t in text:
                self.write(t)
        else:
            raise "Cannot write"

    # Prepends a string s with its length
    def length(self, s):
        self.write(str(len(s)))
        self.write(s)

    def generic_name(self, name):
        self.write("N")
        if type(name) is list:
            for n in name:
                self.length(n)
        else:
            self.length(name)
        self.write("E")

    # Write an integer value, distinguishing between positive and negatives
    def generic_integer(self, num):
        if num < 0:
            self.write("j")
        else:
            self.write("k")
        self.write(str(abs(num)))

    def generic_types(self, name, types):
        m = _Mangle()
        m.generic_name(name)
        for t in types:
            m.visit(t)
        s = "".join(m.mangle)
        self.length(s)

    def generic_variable(self, name, unique):
        self.write("V")
        self.generic_name(name)
        self.generic_integer(unique)

    def generic_function(self, name, arg_types):
        self.write("F")
        self.generic_types(name, arg_types)

    def generic_class(self, name, member_types):
        self.write("C")
        self.generic_types(name, member_types)

    def visit_Arg(self, node):
        self.visit(node.annotation)

    def visit_Unknown(self, node):
        if node.inner:
            self.visit(node.inner)
        else:
            raise "Cannot call visit on unresolved unknown"

    def visit_Boolean(self, node):
        self.write("b")

    def visit_Integer(self, node):
        self.write("i")

    def visit_Char(self, node):
        self.write("c")

    def visit_Floating(self, node):
        self.write("f")

    def visit_ID(self, node):
        self.write("a")

    def visit_Ntuple(self, node):
        self.write("t")
        m = _Mangle()
        for e in node.tuple_types:
            m.visit(e)
        s = "".join(m.mangle)
        self.length(s)

    def visit_Vector(self, node):
        self.write("l")
        self.visit(node.element_type)

    def visit_String(self, node):
        self.write("u")

    def visit_Bytes(self, node):
        self.write("m")

    def visit_Dictionary(self, node):
        self.write("d")
        self.visit(node.key_type)
        self.visit(node.value_type)

    def visit_DynamicSet(self, node):
        self.write("s")
        self.visit(node.element_type)

    def visit_Option(self, node):
        self.write("o")
        self.visit(node.contained_type)

    def visit_Result(self, node):
        self.write("r")
        self.visit(node.ok_type)
        self.visit(node.err_type)

    def visit_UserClass(self, node):
        self.generic_class(node.identifier, node.member_types.values())

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





