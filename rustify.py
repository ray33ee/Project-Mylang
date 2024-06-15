import ast

import ir
from contextlib import contextmanager
import logging
import m_types
import mangler

logger = logging.getLogger(__name__)

# Convert our Rust IR AST into RUst source code
def rustify(p: ir.Module):
    r = _Rustify()
    r.visit(p)

    logger.debug(r.code)

    return "".join(r.code)

class _Rustify(ast.NodeVisitor):

    def __init__(self):
        self.code = []
        self.indent = 0
        self.in_class = False

    def write(self, text):
        self.code.append(text)

    def fill(self, text=""):
        self.write("\n")
        self.write("    " * self.indent + text)

    @contextmanager
    def block(self):
        self.write(" {")
        self.indent += 1
        yield
        self.indent -= 1
        self.fill("}")

    @contextmanager
    def class_block(self):
        self.in_class = True
        yield
        self.in_class = False


    @contextmanager
    def delimit(self, start, end):
        self.write(start)
        yield
        self.write(end)

    @contextmanager
    def statement(self):
        self.fill()
        yield
        self.write(";")

    def traverse(self, node):
        if type(node) is list:
            for n in node:
                self.traverse(n)
        else:
            self.visit(node)

    def write_mangled(self, item):

        import mangler

        m = mangler.Mangle(item)

        self.write(str(m))

    def comma_separated(self, node, start="(", end=")", separator=", ", prepend=""):
        with self.delimit(start, end):
            self.write(prepend)
            comma = False
            for n in node:
                if comma:
                    self.write(separator)
                else:
                    comma = True
                self.traverse(n)


    def visit_Arg(self, node):
        self.traverse(node.expr)
        self.write(": ")
        self.traverse(node.annotation)

    def visit_Member(self, node):
        self.write(node.id)
        self.write(": ")
        self.traverse(node.annotation)

    def visit_Boolean(self, node):
        self.write("bool")

    def visit_Integer(self, node):
        self.write("i64")

    def visit_Floating(self, node):
        return self.write("f64")

    def visit_Char(self, node):
        raise NotImplemented()

    def visit_ID(self, node):
        self.write("usize")

    def visit_Ntuple(self, node):
        self.comma_separated(node.tuple_types)

    def visit_Vector(self, node):
        self.write("Vec")
        logger.warning("Rustifying a m_type.Vector is not implemented yet")

    def visit_String(self, node):
        self.write("String")

    def visit_Bytes(self, node):
        raise NotImplemented()

    def visit_Dictionary(self, node):
        raise NotImplemented()

    def visit_DynamicSet(self, node):
        raise NotImplemented()

    def visit_Option(self, node):
        self.write("Option")
        self.comma_separated([node.contained_type], "<", ">")

    def visit_Result(self, node):
        self.write("Result")
        self.comma_separated([node.ok_type, node.err_type], "<", ">")

    def visit_UserClass(self, node):
        self.write("_Z"+node.mangle())

    def visit_Module(self, node):
        self.traverse(node.functions)
        self.traverse(node.classes)

    def visit_ClassDef(self, node):
        self.fill()
        self.write("struct ")
        self.write_mangled(node)
        with self.block():
            self.fill()
            self.comma_separated(node.member_map, "", "", ", \n    ")

        self.fill()
        self.write("impl ")
        self.write_mangled(node)
        with self.block():
            with self.class_block():
                self.traverse(node.functions)

    def generic_function(self, node, is_main=False, prepend="", members=None):
        self.fill()
        self.write("fn ")

        if is_main:
            self.write("main")
        else:
            self.write_mangled(node)

        self.comma_separated(node.args, prepend=prepend)

        if node.ret_type.mangle() != "t0" or members:  # If the return type is not unit type, (), display it
            self.write(" -> ")
            if members:
                self.write("Self")
            else:
                self.traverse(node.ret_type)
        with self.block():
            self.traverse(node.body)

            if members:
                self.fill()
                self.write("Self ")
                with self.block():
                    for n in members:
                        self.fill()
                        self.write(n)
                        self.write(": ")
                        self.write(mangler.MemberVariable(n).mangle())
                        self.write(",")


    def visit_FunctionDef(self, node):
        self.generic_function(node)

    def visit_MainFunctionDef(self, node):
        self.generic_function(node, is_main=True)

    def visit_MemberFunctionDef(self, node):

        if len(node.args) == 0:
            prepend = "& mut self"
        else:
            prepend = "& mut self, "

        self.generic_function(node, prepend=prepend)

    def visit_InitFunctionDef(self, node):
        self.generic_function(node, members=node.member_list)



    def visit_GetterAssign(self, node):
        with self.statement():
            self.write("self.")
            self.write(node.self_id)
            self.write(" = ")
            self.traverse(node.value)


    def visit_LetAssign(self, node):
        with self.statement():
            self.write("let mut ")
            self.traverse(node.target)
            self.write(" = ")
            self.traverse(node.value)

    def visit_Reassign(self, node):
        with self.statement():
            self.traverse(node.target)
            self.write(" = ")
            self.traverse(node.value)

    def visit_Break(self, node):
        with self.statement():
            self.write("break")

    def visit_Continue(self, node):
        with self.statement():
            self.write("continue")

    def visit_Return(self, node):
        with self.statement():
            self.write("return ")
            self.traverse(node.expr)

    def visit_Expr(self, node):
        with self.statement():
            self.traverse(node.expr)

    def visit_For(self, node):
        self.fill()
        self.write("for ")
        self.traverse(node.target)
        self.write(" in ")
        self.traverse(node.iterator)
        with self.block():
            self.traverse(node.body)

    def visit_While(self, node):
        self.fill()
        self.write("while ")
        self.traverse(node.condition)
        with self.block():
            self.traverse(node.body)

    def visit_IfElse(self, node):
        self.fill()
        self.write("if ")
        self.traverse(node.condition)
        with self.block():
            self.traverse(node.if_block)
        if len(node.else_block) > 0:
            self.fill()
            self.write("else ")
            with self.block():
                self.traverse(node.else_block)

    def visit_ClassConstructor(self, node):
        from mangler import Mangle
        self.write_mangled(node.usr_class)
        self.write("::")

        self.write(str(Mangle(ir.FunctionDef("__init__", node.types))))
        self.comma_separated(node.args)

    def visit_IRTuple(self, node):
        self.comma_separated(node.elements)

    def visit_Identifier(self, node):
        self.write(node.id)

    def visit_SelfVariable(self, node):
        self.write("self.")
        self.write(node.id)

    def visit_SelfFunction(self, node):
        self.write("self.")
        self.write_mangled(node)
        self.comma_separated(node.args)

    def visit_MemberFunction(self, node):
        self.traverse(node.expr)
        self.write(".")
        self.write_mangled(node)
        self.comma_separated(node.args)

    def visit_Constant(self, node):
        if type(node.value) is str:
            self.write(f'"{str(node.value)}"')
        elif type(node.value) is bool:
            self.write(str(node.value).lower())
        else:
            self.write(str(node.value))

    def visit_Tuple(self, node):
        self.comma_separated(node.elements)

    def visit_SolitarySelf(self, node):
        self.write("self")
        logger.warning("Solitary self is not implemented yet. Rustified code may not work as expected")

    def visit_GlobalFunctionCall(self, node):
        self.write_mangled(node)
        self.comma_separated(node.args)





