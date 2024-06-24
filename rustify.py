import ast

import ir
from contextlib import contextmanager
import logging

import m_types
import mangle

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
        if type(text) is str:
            self.code.append(text)
        else:
            raise "Write can only write strings"

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

        import mangle

        m = mangle.mangle(item)

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

    def heap_wrapper(self, identifier):
        self.write("heap::CellGc<")
        self.write(identifier)
        self.write(">")


    @contextmanager
    def new_heap(self):

        self.write("heap::new_gc(")
        yield
        self.write(")")

    @contextmanager
    def access_heap(self):
        self.write("heap::mut_ref_gc(&")
        yield
        self.write(")")


    def visit_Unknown(self, node):
        if node.has_inner():
            self.visit(node.inner())
        else:
            raise "Cannot rustify empty unknown"

    def visit_Arg(self, node):
        self.write("mut ")
        self.write(node.id)
        self.write(": ")
        self.traverse(node.annotation)

    def visit_Member(self, node):
        self.write(node.id)
        self.write(": ")
        self.traverse(node.annotation)

    def visit_Boolean(self, node):
        self.write("built_ins::bool::Bool")

    def visit_Integer(self, node):
        self.write("built_ins::integer::Integer")

    def visit_Floating(self, node):
        return self.write("built_ins::float::Float")

    def visit_Char(self, node):
        raise NotImplemented()

    def visit_ID(self, node):
        self.write("usize")

    def visit_Ntuple(self, node):
        self.comma_separated(node.tuple_types)

    def visit_Vector(self, node):
        self.write("built_ins::list::List<")
        self.traverse(node.element_type)
        self.write(">")

    def visit_String(self, node):
        self.write("built_ins::string::String")

    def visit_Bytes(self, node):
        raise NotImplemented()

    def visit_Dictionary(self, node):
        raise NotImplemented()

    def visit_DynamicSet(self, node):
        raise NotImplemented()

    def visit_Option(self, node):
        self.write("crate::built_ins::option::Option")
        self.comma_separated([node.contained_type], "<", ">")

    def visit_Result(self, node):
        self.write("Result")
        self.comma_separated([node.ok_type, node.err_type], "<", ">")

    def visit_UserClass(self, node):
        self.heap_wrapper(mangle.mangle(node))
        #self.write(mangle.mangle(node))

    def visit_Module(self, node):
        self.traverse(node.functions)
        self.traverse(node.classes)

    def visit_CyclicClassDef(self, node):
        self.fill()
        self.write("#[derive(dumpster::Collectable)]")
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

        if node.ret_type != m_types.Ntuple([]) or members:  # If the return type is not unit type, (), display it
            self.write(" -> ")
            if members:
                self.heap_wrapper("Self")
            else:
                self.traverse(node.ret_type)

        with self.block():
            self.traverse(node.body)

            if members:
                self.fill()
                with self.new_heap():
                    self.write("Self ")
                    with self.block():
                        for n in members:
                            self.fill()
                            self.write(n)
                            self.write(": ")
                            self.write(mangle.mangle(mangle.MemberVariable(n)))
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
        self.write_mangled(node.usr_class)
        self.write("::")

        self.write(str(mangle.mangle(ir.FunctionDef("__init__", node.types))))
        self.comma_separated(node.args)

    def visit_IRTuple(self, node):
        self.comma_separated(node.elements)

    def visit_Identifier(self, node):
        self.write(node.id)

    def visit_CloneIdentifier(self, node):
        self.write(node.id)
        self.write(".clone()")

    def visit_SelfVariable(self, node):
        self.write("self.")
        self.write(node.id)
        if node.to_clone:
            self.write(".clone()")

    def visit_SelfFunction(self, node):
        self.write("self.")
        self.write_mangled(node)
        self.comma_separated(node.args)

    def visit_UserClassMemberFunction(self, node):
        with self.access_heap():
            self.traverse(node.expr)
        self.write(".")
        self.write_mangled(node)
        self.comma_separated(node.args)

    def visit_BuiltInMemberFunction(self, node):
        self.traverse(node.expr)
        self.write(".")
        self.write_mangled(node)
        self.comma_separated(node.args)

    def visit_Constant(self, node):
        if type(node.value) is str:
            self.write(f'crate::built_ins::string::String::new(std::string::String::from("{str(node.value)}"))')
        elif type(node.value) is bool:
            self.write("built_ins::bool::Bool::new(")
            self.write(str(node.value).lower())
            self.write(")")
        elif type(node.value) is int:
            self.write("built_ins::integer::Integer::new(")
            self.write(str(node.value))
            self.write(")")
        elif type(node.value) is float:
            self.write("built_ins::float::Float::new(")
            self.write(str(node.value))
            self.write(")")
        else:
            self.write(str(node.value))

    def visit_Tuple(self, node):
        self.comma_separated(node.elements)

    def visit_List(self, node):
        self.write("built_ins::list::List::new(vec!")
        self.comma_separated(node.elements, start='[', end=']')
        self.write(")")

    def visit_SolitarySelf(self, node):
        self.write("heap::filthy_cast_to_gc(&self)")

    def visit_GlobalFunctionCall(self, node):
        self.write_mangled(node)
        self.comma_separated(node.args)

    def visit_JoinedString(self, node):
        mangled_string_name = mangle.mangle(node)
        self.write("{ ")
        self.write(f"let mut {mangled_string_name} = crate::built_ins::string::String::new(std::string::String::new()); ")
        for value in node.values:
            if type(value) is ir.Constant:
                if type(value.value) is str:
                    self.write(mangled_string_name + '.push_slice("')
                    self.write(value.value)
                    self.write('"); ')
                else:
                    raise "joined string value is not a constant string"
            elif type(value) is ir.FormattedValue:
                self.traverse(value.value)
                self.write(f"._ZF18N12__push_fmt__Eui({mangled_string_name}.clone(), crate::built_ins::integer::Integer::new(0)); ")
            else:
                raise "joined string value is not a constant or formatted value"
        self.write(f"{mangled_string_name} }}")

    def visit_SomeCall(self, node):
        self.write("crate::built_ins::option::Option::new(std::option::Option::Some(")
        self.traverse(node.expr)
        self.write("))")






