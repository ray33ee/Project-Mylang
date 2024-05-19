import ast

import custom_nodes


def sugar(node: ast.AST):
    return _Sugar().visit(node)

class _Sugar(ast.NodeTransformer):

    built_in_set = {"float", "int", "complex", "id", "char", "str", "repr", "bool", "abs", "len", "iter",
                    "next", "path", "real", "imag", "bytes"}

    def __init__(self):
        super().__init__()
        self.working_function = None
        self.working_class = None


    # Returns true if the function in self.working_function represents a class constructor
    def function_is_class_init(self):
        if self.working_class:
            if self.working_function:
                if self.working_function.name == "__init__":
                    return True
        return False

    # Returns true if the function in self.working_function represents a class getter or setter of the variable named
    # 'identifier'. If identifier is None, then the function return true if the function is any getter or setter
    def function_is_getter_or_setter(self, identifier=None):
        if self.working_class:
            if self.working_function:
                fname = self.working_function.name
                if (fname[:6] == "__get_" or fname[:6] == "__set_") and fname[-2:] == "__":
                    if identifier:
                        return fname[7:-2] == identifier
                    else:
                        return True
        return False

    # Returns true if the node is within a class
    def is_in_class(self):
        return bool(self.working_class)

    def traverse(self, node):
        if isinstance(node, list):
            return [self.traverse(n) for n in node]
        else:
            return super().visit(node)

    # Chooses between a MemberFunction and SelfMemberFuncton
    def member_function(self, expr: ast.expr, id: str, args):
        if isinstance(expr, ast.Name):
            if expr.id == "self" and self.is_in_class():
                return custom_nodes.SelfMemberFunction(id, self.traverse(args))
        return custom_nodes.MemberFunction(self.traverse(expr), id, self.traverse(args))



    def visit_FunctionDef(self, node):
        self.working_function = node
        f = ast.FunctionDef(node.name, node.args, self.traverse(node.body), node.decorator_list, node.returns, node.type_comment, node.type_params)
        ast.fix_missing_locations(f)
        self.working_function = None
        return f

    def visit_ClassDef(self, node):
        self.working_class = node
        c = ast.ClassDef(node.name, node.bases, node.keywords, self.traverse(node.body), node.decorator_list, node.type_params)
        ast.fix_missing_locations(c)
        self.working_class = None
        return c

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):

            # Convert float(x) into x.__float__(). More generically, given the function f,
            # f(x1, x2, ..., xn) maps to x1.__f__(x2, ..., xn)
            if node.func.id in self.built_in_set:
                # The function must have at least one argument
                assert len(node.args) != 0

                return self.member_function(node.args[0], f"__{node.func.id}__", node.args[1:])

            return custom_nodes.MyCall(node.func.id, self.traverse(node.args))
        elif isinstance(node.func, ast.expr):

            if isinstance(node.func, ast.Attribute):

                return self.member_function(node.func.value, node.func.attr, node.args)

            # If the function is an expression instead of a node, then if expr is the expression, what we have is
            # expr(...) which must evaluate to expr.__call__(...)
            return self.member_function(node.func, "__call__", node.args)

    def visit_Attribute(self, node):
        if isinstance(node.value, ast.Name):
            if node.value.id == "self" and (self.function_is_class_init() or self.function_is_getter_or_setter()):
                return custom_nodes.SelfMemberVariable(node.attr)

        if isinstance(node.value, ast.expr):
            return self.member_function(node.value, f"__get_{node.attr}__", [])

    def visit_Assign(self, node):
        # We don't support chained assignment just yet
        assert len(node.targets) == 1

        # get LHS
        lhs = node.targets[0]

        if isinstance(lhs, ast.Attribute):
            if not self.function_is_class_init() and not self.function_is_getter_or_setter(lhs.attr):
                #a.b = e
                # a.__set_b__(e)
                return ast.Expr(self.member_function(lhs.value, f"__set_{lhs.attr}__", [node.value]))
        if isinstance(lhs, ast.Subscript):
            # convert a[b] = c into a.__setitem__(b, c)
            return ast.Expr(self.member_function(lhs.value, "__setitem__", [lhs.slice, node.value]))


        a = ast.Assign([self.traverse(lhs)], self.traverse(node.value), node.type_comment)
        ast.fix_missing_locations(a)

        return a

    def visit_BinOp(self, node):
        binary_op_mapping = {
            ast.Add: "__add__",
            ast.Sub: "__sub__",
            ast.Mult: "__mul__",
            ast.Div: "__truediv__",
            ast.Mod: "__mod__",
            ast.Pow: "__pow__",
            ast.LShift: "__lshift__",
            ast.RShift: "__rshift__",
            ast.BitOr: "__or__",
            ast.BitXor: "__xor__",
            ast.BitAnd: "__and__",
            ast.FloorDiv: "__floordiv__",

        }

        return self.member_function(node.left, binary_op_mapping[type(node.op)], [node.right])

    def visit_UnaryOp(self, node):
        unary_op_mapping = {
            ast.Invert: "__invert__",
            ast.UAdd: "__pos__",
            ast.USub: "__neg__"
        }

        return self.member_function(node.operand, unary_op_mapping[type(node.op)], [])

    def visit_Compare(self, node):
        # Mylang does not support chained comparison
        assert len(node.ops) == 1
        assert len(node.comparators) == 1

        compare_op_mapping = {
            ast.Eq: "__eq__",
            ast.NotEq: "__ne__",
            ast.Lt: "__lt__",
            ast.LtE: "__le__",
            ast.Gt: "__gt__",
            ast.GtE: "__ge__",
        }

        left = node.left
        op = node.ops[0]
        right = node.comparators[0]

        # Replace a is b with a.__id__().__eq__(b.__id__())
        # Replace a in b with b.__contains__(a)
        # Add an extra negate for the Not varieties
        if (op is ast.Is) or (op is ast.IsNot) or (op is ast.In) or (op is ast.NotIn):
            raise NotImplemented

        return self.member_function(left, compare_op_mapping[type(op)],
                                           [right])

    def visit_Slice(self, node):
        # replace a slice a:b:c with slice(a, b, c)
        # We need to think about how we will represent 'None' in mylang before we finish this
        raise NotImplemented


    def visit_Subscript(self, node):
        return self.member_function(node.value, "__getitem__", [node.slice])

    def visit_Name(self, node):
        if node.id == "self" and self.is_in_class():
            return custom_nodes.SolitarySelf()
        else:
            return node