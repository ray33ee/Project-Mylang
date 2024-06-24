import ast

import custom_nodes
import m_types


def sugar(node: ast.AST):
    return _Sugar().visit(node)


class _Sugar(ast.NodeTransformer):

    built_in_set = {"float", "int", "complex", "id", "char", "str", "repr", "bool", "abs", "len", "iter",
                    "next", "path", "real", "imag", "bytes", "zero", "one"}

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
                        return fname[6:-2] == identifier
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

    def flatten(self, l):
        r = []
        if type(l) is list:
            for item in l:
                r.extend(self.flatten(item))
            return r
        else:
            return [l]

    # Chooses between a MemberFunction and SelfMemberFuncton
    def member_function(self, expr: ast.expr, id: str, args):
        if isinstance(expr, ast.Name):
            if expr.id == "self" and self.is_in_class():
                return custom_nodes.SelfMemberFunction(id, self.traverse(args))
        return custom_nodes.MemberFunction(self.traverse(expr), id, self.traverse(args))


    def visit_arguments(self, node):
        a = ast.arguments(args=self.traverse(node.args), posonlyargs=node.posonlyargs, defaults=node.defaults, kwonlyargs=node.kwonlyargs)
        ast.fix_missing_locations(a)

        return a


    def resolve_annotation(self, annotation):

        if not annotation:
            return m_types.WildCard()
        if type(annotation) is ast.Constant:
            if annotation.value == ...:
                return m_types.WildCard()
            else:
                raise "Invalid annotation expression"
        elif type(annotation) is ast.Tuple:
            return [self.resolve_annotation(x) for x in annotation.elts]
        elif type(annotation) is ast.Name:
            if annotation.id == "int":
                return m_types.Integer()
            elif annotation.id == "float":
                return m_types.Floating()
            elif annotation.id == "bool":
                return m_types.Boolean()
            elif annotation.id == "char":
                return m_types.Char()
            elif annotation.id == "id":
                return m_types.ID()
            elif annotation.id == "bytes":
                return m_types.Bytes()
            elif annotation.id == "str":
                return m_types.String()
            elif annotation.id == "list":
                return m_types.Vector(m_types.WildCard)
            elif annotation.id == "tuple":
                raise "Tuple must contain types or wildcards. tuple[...] where ... represents a wildcard for any type"
            elif annotation.id == "dict":
                return m_types.Dictionary(m_types.WildCard, m_types.WildCard)
            elif annotation.id == "set":
                return m_types.DynamicSet(m_types.WildCard)
            elif annotation.id == "option":
                return m_types.Option(m_types.WildCard)
            elif annotation.id == "result":
                return m_types.Result(m_types.WildCard, m_types.WildCard)
            else:
                raise "Argument annotation (Name) not recognised"
        elif type(annotation) is ast.Subscript:

            if type(annotation.value) is ast.Name:
                if annotation.value.id == "list":
                    return m_types.Vector(self.resolve_annotation(annotation.slice))
                elif annotation.value.id == "tuple":
                    return m_types.Ntuple(self.resolve_annotation(annotation.slice))
                elif annotation.value.id == "dict":
                    return m_types.Dictionary(self.resolve_annotation(annotation.slice.elts[0]), self.resolve_annotation(annotation.slice.elts[1]))
                elif annotation.value.id == "set":
                    return m_types.DynamicSet(self.resolve_annotation(annotation.slice))
                elif annotation.value.id == "option":
                    return m_types.Option(self.resolve_annotation(annotation.slice))
                elif annotation.value.id == "result":
                    return m_types.Result(self.resolve_annotation(annotation.slice.elts[0]), self.resolve_annotation(annotation.slice.elts[1]))
                else:
                    raise "Argument annotation (Subscript) not recognised"

            else:
                raise "Invalid annotation expression"

        else:
            raise "Annotation type not recognised (not a Name or Subscript)"


    def visit_arg(self, node):

        annotation = self.resolve_annotation(node.annotation)

        arg = ast.arg(arg=node.arg, annotation=annotation)

        ast.fix_missing_locations(arg)

        return arg

    def visit_FunctionDef(self, node):
        self.working_function = node

        if not self.function_is_class_init():
            f = ast.FunctionDef(node.name, self.traverse(node.args), self.flatten(self.traverse(node.body)), node.decorator_list, node.returns, node.type_comment, node.type_params)
        else:
            f = custom_nodes.InitFunctionDef(self.traverse(node.args), self.flatten(self.traverse(node.body)), node.decorator_list, node.returns, node.type_comment, node.type_params)

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

            # Convert float(x) into x.__float__(). More generically, given the special function f,
            # we map f(x1, x2, ..., xn) to x1.__f__(x2, ..., xn)
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

        # First we note that all Mylang assignments can be written in the form

        # a_1 = a_2 = ... = a_n = b_1[...] = b_2[...] = ... = b_m[...] = expr

        # where a_i are named variables and b_i[...] are subscript assignments.

        # The subscript assignments must be replaced with b_i.__setitem__(..., e).

        # We must convert the single statement above into multiple statements.

        # Note: A special case of the above form is when n=1 and m=0 or n=0 and m=1, i.e. only one target in the
        # assignment and this is handled on its own

        # First, unless we have the special case, we create a mangled temporary variable name and assign 'expr' to it:

        # v = expr

        # Then we create 'n' assignments:

        # a_1 = v
        # a_2 = v
        # ...
        # a_n = v

        # Then we create 'm' __setitem__ calls:

        # b_1.__setitem__(..., v)
        # b_2.__setitem__(..., v)
        # ...
        # b_m.__setitem__(..., v)

        def handle_target(target, rhs):
            if type(target) is ast.Subscript:
                n = ast.Expr(custom_nodes.MemberFunction(self.traverse(target.value), "__setitem__", [self.traverse(target.slice), rhs]))
                ast.fix_missing_locations(n)
                return n
            elif type(target) is ast.Attribute:

                if type(target.value) is ast.Name:
                    if target.value.id == "self":
                        if self.function_is_getter_or_setter(target.attr):
                            return custom_nodes.GetterAssign(target.attr, rhs)
                        elif self.function_is_class_init():
                            return custom_nodes.InitAssign(target.attr, rhs)

                return ast.Expr(
                    self.member_function(target.value, f"__set_{target.attr}__", [rhs]))
            else:
                n = custom_nodes.MonoAssign(self.traverse(target), rhs)
                ast.fix_missing_locations(n)
                return n


        if len(node.targets) == 1:

            # If we have a single, non-chained assignment we can easily convert this into a MonoAssign

            target = node.targets[0]

            return handle_target(target, self.traverse(node.value))

        else:

            # We outline a formal algorithm as follows:

            # 1. Create an empty list, which will represent the list of assignment nodes
            # 2. Create a mangled variable name
            # 3. Create an assignment with the temporary variable as the sole target and the expr as the value.
            # 4. Iterate over each target.
            #     i. If the target is a Name, add 'Name = v' as an assignment to the list
            #    ii. If the target is a subscript, add the __setitem__ call to the list
            # 5. Return the list of nodes

            # 1.
            assigns = []

            import mangle
            # 2.
            mangled_name = mangle.mangle(node)

            # 3.
            tmp_assigner = custom_nodes.MonoAssign(ast.Name(mangled_name, ast.Store()), self.traverse(node.value))

            ast.fix_missing_locations(tmp_assigner)

            assigns.append(tmp_assigner)

            # 4.

            for target in node.targets:
                assigns.append(handle_target(target, ast.Name(mangled_name, ast.Store())))

            # 5.

            return assigns
        
    def visit_If(self, node):
        condition = custom_nodes.MemberFunction(self.traverse(node.test), "__bool__", [])
        return ast.If(condition, self.traverse(node.body), self.traverse(node.orelse))

    def visit_While(self, node):
        condition = custom_nodes.MemberFunction(self.traverse(node.test), "__bool__", [])
        return ast.While(condition, self.traverse(node.body), self.traverse(node.orelse))

    def visit_For(self, node):
        iter = custom_nodes.MemberFunction(self.traverse(node.iter), "__iter__", [])
        return ast.For(self.traverse(node.target), iter, self.traverse(node.body), self.traverse(node.orelse))

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
            raise NotImplemented()

        return self.member_function(left, compare_op_mapping[type(op)], [right])

    def visit_Slice(self, node):
        # replace a slice a:b:c with slice(a, b, c)
        # We need to think about how we will represent 'None' in mylang before we finish this
        raise NotImplemented()

    def visit_Subscript(self, node):
        return self.member_function(node.value, "__getitem__", [node.slice])

    def visit_Name(self, node):
        if node.id == "self" and self.is_in_class():
            return custom_nodes.SolitarySelf()
        else:
            return node

    def visit_FormattedValue(self, node):
        return ast.FormattedValue(self.traverse(node.value), node.conversion)

