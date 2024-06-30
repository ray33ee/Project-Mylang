import ast

import m_types
import mangle


def unparse(ast_obj):
    unparser = _Unparser()
    return unparser.visit(ast_obj)

# Reimplements ast's _Unparser to work with our custom AST nodes.
# Not needed during translation but useful for debugging

class _Unparser(ast._Unparser):
    def __init__(self,  _avoid_backslashes=False):
        super().__init__()

    def visit_arg(self, node):

        self.write(node.arg)

        if type(node.annotation) is not m_types.WildCard:
            self.write(": ")
            self.traverse(node.annotation)

    def visit_InitFunctionDef(self, node):
        self.visit_FunctionDef(node)

    def visit_DelFunctionDef(self, node):
        self.visit_FunctionDef(node)

    def visit_Integer(self, node):
        self.write("int")

    def visit_Floating(self, node):
        self.write("float")

    def visit_String(self, node):
        self.write("str")

    def visit_ID(self, node):
        self.write("id")

    def visit_Bytes(self, node):
        self.write("bytes")

    def visit_Boolean(self, node):
        self.write("bool")

    def visit_Char(self, node):
        self.write("char")

    def visit_Vector(self, node):
        self.write("list[")
        self.traverse(node.element_type)
        self.write("]")

    def visit_DynamicSet(self, node):
        self.write("set[")
        self.traverse(node.element_type)
        self.write("]")

    def visit_Ntuple(self, node):
        raise NotImplemented()

    def visit_Result(self, node):
        raise NotImplemented()

    def visit_Option(self, node):
        raise NotImplemented()

    def visit_Dictionary(self, node):
        raise NotImplemented()

    def visit_SolitarySelf(self, node):
        self.write("SOLITARYself")

    def visit_SelfMemberFunction(self, node):
        self.write("self.")
        self.write(node.id)
        with self.delimit("(", ")"):
            comma = False
            for a in node.args:
                if comma:
                    self.write(", ")
                else:
                    comma = True
                self.traverse(a)
    def visit_SelfMemberVariable(self, node):
        self.write("self.")
        self.write(node.id)

    def visit_MemberFunction(self, node):
        self.write("(")
        self.traverse(node.exp)
        self.write(")")
        self.write(".")
        self.write(node.id)
        with self.delimit("(", ")"):
            comma = False
            for a in node.args:
                if comma:
                    self.write(", ")
                else:
                    comma = True
                self.traverse(a)

    def visit_GetterAssign(self, node):
        self.fill()
        self.write("self.")
        self.write(node.self_id)
        self.write(" = ")
        self.traverse(node.value)

    def visit_InitAssign(self, node):

        self.fill()
        self.write(mangle.mangle(node))
        self.write(" = ")
        self.traverse(node.value)

    def visit_MyCall(self, node):
        self.write(node.id)
        with self.delimit("(", ")"):
            comma = False
            for a in node.args:
                if comma:
                    self.write(", ")
                else:
                    comma = True
                self.traverse(a)

    def visit_MonoAssign(self, node):
        self.fill()
        self.traverse(node.target)
        self.write(" = ")
        self.traverse(node.value)

    def visit_WildCard(self, node):
        self.write("...")

    def visit_Integer(self, node):
        self.write("int")

    def visit_Boolean(self, node):
        self.write("bool")

    def visit_Floating(self, node):
        self.write("float")

    def visit_Char(self, node):
        self.write("char")

    def visit_ID(self, node):
        self.write("id")

    def visit_Ntuple(self, node):
        self.write("tuple")
        with self.delimit("[", "]"):
            comma = False
            for a in node.tuple_types:
                if comma:
                    self.write(", ")
                else:
                    comma = True
                self.traverse(a)

    def visit_Vector(self, node):
        self.write("list")
        with self.delimit("[", "]"):
            self.visit(node.element_type)

    def visit_String(self, node):
        self.write("str")

    def visit_Bytes(self, node):
        self.write("bytes")

    def visit_Dictionary(self, node):
        self.write("dict")
        with self.delimit("[", "]"):
            self.traverse(node.key_type)
            self.write(", ")
            self.traverse(node.value_type)

    def visit_DynamicSet(self, node):
        self.write("set")
        with self.delimit("[", "]"):
            self.visit(node.element_type)

    def visit_Option(self, node):
        self.write("option")
        with self.delimit("[", "]"):
            self.visit(node.contained_type)

    def visit_Result(self, node):
        self.write("result")
        with self.delimit("[", "]"):
            self.traverse(node.ok_type)
            self.write(", ")
            self.traverse(node.err_type)


