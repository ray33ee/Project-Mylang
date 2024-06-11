import ast

import ir
from contextlib import contextmanager

# Convert our Rust IR AST into RUst source code
def rustify(p: ir.Module):
    r = _Rustify()
    r.visit(p)

    print(r.code)

    return "".join(r.code)

class _Rustify(ast.NodeVisitor):

    def __init__(self):
        self.code = []
        self.indent = 0

    def write(self, *text):
        self.code.extend(text)

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

    def comma_separated(self, node, start="(", end=")", separator=", "):
        with self.delimit(start, end):
            for n in node:
                self.traverse(n)
                self.write(separator)

    def visit_Module(self, node):
        self.traverse(node.functions)
        self.traverse(node.classes)

    def visit_ClassDef(self, node):
        pass

    def visit_FunctionDef(self, node):
        self.write("fn ")
        self.write_mangled(node)

        raise "node.args is a OrderedDict and not an AST node, so we have trouble traversing it"
        # node.args is a
        self.comma_separated(node.args)



        if node.ret_type.mangle() != "t0":  # If the return type is not unit type, (), display it
            self.write(" -> ")
            self.traverse(node.ret_type)
        with self.block():
            self.traverse(node.body)

    def visit_LetAssign(self, node):
        with self.statement():
            self.write("let mut ")
            self.write(node.target.id)
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
        self.write(str(node.value))

    def visit_SolitarySelf(self, node):
        raise "Solitary self thing not done yet"

    def visit_GlobalFunctionCall(self, node):
        self.write_mangled(node)
        self.comma_separated(node.args)




