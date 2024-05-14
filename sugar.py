import utils
import ast
import errors
import custom_nodes
import gc

# The code in sugar converts syntactic sugar into their equivalent function calls and converts certain nodes into
# our own custom nodes for easier parsing later

def recursive_resolve_special_functions_expression(expression, super_class: ast.ClassDef, super_function: ast.FunctionDef):

    built_in_set = {"float", "int", "complex", "id", "char", "str", "repr", "bool", "abs", "len", "iter", "next",
                    "path", "real", "imag", "bytes"}

    unary_op_mapping = {
        ast.Invert: "__invert__",
        ast.UAdd: "__pos__",
        ast.USub: "__neg__"
    }

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

    compare_op_mapping = {
        ast.Eq: "__eq__",
        ast.NotEq: "__ne__",
        ast.Lt: "__lt__",
        ast.LtE: "__le__",
        ast.Gt: "__gt__",
        ast.GtE: "__ge__",
    }

    if type(expression) is ast.BoolOp:
        raise NotImplemented
    elif type(expression) is ast.BinOp:
        if type(expression.left) is ast.Name:
            if expression.left.id == "self":
                raise NotImplemented

        return custom_nodes.MemberFunction(recursive_resolve_special_functions_expression(expression.left, super_class, super_function), binary_op_mapping[type(expression.op)], [recursive_resolve_special_functions_expression(expression.right, super_class, super_function)])
        return ast.Call(
            ast.Attribute(recursive_resolve_special_functions_expression(expression.left, super_class, super_function), binary_op_mapping[type(expression.op)], ast.Load()),
            [recursive_resolve_special_functions_expression(expression.right, super_class, super_function)],
            [])
    elif type(expression) is ast.Attribute:

        if type(expression.value) is ast.Name:

            if expression.value.id == 'self':

                if super_class is not None:
                    if super_function.name == "__init__":
                        return custom_nodes.SelfMemberVariable(expression.attr)
                    if (super_function.name[:6] == "__get_" or super_function.name[:6] == "__set_") and super_function.name[-2:] == "__":
                        return custom_nodes.SelfMemberVariable(expression.attr)

                return custom_nodes.SelfMemberFunction(f"__get_{expression.attr}__", [])




        return custom_nodes.MemberFunction(recursive_resolve_special_functions_expression(expression.value, super_class, super_function), f"__get_{expression.attr}__", [])

        return ast.Call(ast.Attribute(recursive_resolve_special_functions_expression(expression.value, super_class, super_function),
                                      f"__get_{expression.attr}__", expression.ctx), [], [])
    elif type(expression) is ast.UnaryOp:

        if type(expression.operand) is ast.Name:
            if expression.operand.id == "self":
                return custom_nodes.SelfMemberFunction(unary_op_mapping[type(expression.op)], [])

        return custom_nodes.MemberFunction(recursive_resolve_special_functions_expression(expression.operand, super_class, super_function), unary_op_mapping[type(expression.op)], [])
    elif type(expression) is ast.Compare:

        if len(expression.ops) != 1 or len(expression.comparators) != 1:
            raise errors.WrongNumberOfComparisons

        left = recursive_resolve_special_functions_expression(expression.left, super_class, super_function)
        right = recursive_resolve_special_functions_expression(expression.comparators[0], super_class, super_function)

        op_type = type(expression.ops[0])

        # Replace a is b with a.__id__().__eq__(b.__id__())
        # Replace a in b with b.__contains__(a)
        # Add an extra negate for the Not varieties
        if (op_type is ast.Is) or (op_type is ast.IsNot) or (op_type is ast.In) or (op_type is ast.NotIn):
            raise NotImplemented

        if type(left) is ast.Name:
            if left.id == "self":
                return custom_nodes.SelfMemberFunction(compare_op_mapping[op_type], [right])

        return custom_nodes.MemberFunction(left, compare_op_mapping[op_type], [right])


    elif type(expression) is ast.Call:
        if type(expression.func) is ast.Name:
            func_name = expression.func.id

            if func_name in built_in_set:
                # replace FUNCTION(x) with x.__FUNCTION__()

                if type(expression.args[0]) is ast.Name:
                    if expression.args[0].id == "self":
                        return custom_nodes.SelfMemberFunction(f"__{func_name}__", [])
                        return ast.Call(ast.Attribute(recursive_resolve_special_functions_expression(expression.args[0], super_class, super_function), f"__{func_name}__", ast.Load()), [], [])

                return custom_nodes.MemberFunction(recursive_resolve_special_functions_expression(expression.args[0], super_class, super_function), f"__{func_name}__", [])
                return ast.Call(ast.Attribute(recursive_resolve_special_functions_expression(expression.args[0], super_class, super_function), f"__{func_name}__", ast.Load()), [], [])
            else:
                return custom_nodes.MyCall(expression.func.id, [recursive_resolve_special_functions_expression(x, super_class, super_function) for x in expression.args])
                #return ast.Call(expression.func, [recursive_resolve_special_functions_expression(x, super_class, super_function) for x in expression.args], expression.keywords)
        elif type(expression.func) is ast.Attribute:
            #a = ast.Attribute(recursive_resolve_special_functions_expression(expression.func.value, super_class, super_function), expression.func.attr, expression.func.ctx

            print(ast.dump(expression))

            return custom_nodes.MemberFunction(recursive_resolve_special_functions_expression(expression.func.value, super_class, super_function), expression.func.attr, [recursive_resolve_special_functions_expression(x, super_class, super_function) for x in expression.args])
            return ast.Call(a,
                            [recursive_resolve_special_functions_expression(x, super_class, super_function) for x in expression.args], expression.keywords)
        else:
            raise NotImplemented
    elif type(expression) is ast.IfExp:
        return ast.IfExp(
            recursive_resolve_special_functions_expression(expression.test, super_class, super_function),
            recursive_resolve_special_functions_expression(expression.body, super_class, super_function),
            recursive_resolve_special_functions_expression(expression.orelse, super_class, super_function)
        )
    elif type(expression) is ast.Subscript:
        if type(expression.ctx) == ast.Load:

            if type(expression.value) is ast.Name:
                if expression.value.id == "self":
                    return custom_nodes.SelfMemberFunction("__getitem__", [recursive_resolve_special_functions_expression(expression.slice, super_class, super_function)])

            return custom_nodes.MemberFunction(recursive_resolve_special_functions_expression(expression.value, super_class, super_function),
                  "__getitem__", [recursive_resolve_special_functions_expression(expression.slice, super_class, super_function)])
        elif type(expression.ctx) == ast.Store:
            raise "Expressions shouldn't store Subscript things. If there is an exception to this i'd love to know..."
        else:
            raise BaseException

    elif type(expression) is ast.Set:
        raise NotImplemented
    elif type(expression) is ast.Dict:
        raise NotImplemented
    elif type(expression) is ast.List:
        raise NotImplemented
    elif type(expression) is ast.Compare:
        raise NotImplemented
    elif type(expression) is ast.Name:

        if super_class is not None:
            if expression.id == "self":
                return custom_nodes.SolitarySelf()

        return expression
    elif type(expression) is type(expression) is ast.Constant:
        return expression
    elif type(expression) is ast.Slice:



        if expression.lower:
            lower = recursive_resolve_special_functions_expression(expression.lower, super_class, super_function)
        else:
            lower = ast.Constant(None)

        if expression.upper:
            upper = recursive_resolve_special_functions_expression(expression.upper, super_class, super_function)
        else:
            upper = ast.Constant(None)

        if expression.step:
            step = recursive_resolve_special_functions_expression(expression.step, super_class, super_function)
        else:
            step = ast.Constant(None)

        return custom_nodes.MyCall("slice", [lower, upper, step])
        return ast.Call(ast.Name("slice", ast.Load()), [lower, upper, step], [])
    else:
        raise errors.ASTExpressionNotSupported(expression)


def recursive_resolve_special_functions_statement(statement, super_class, super_function):

    if type(statement) is ast.Assign:
        statement.value = recursive_resolve_special_functions_expression(statement.value, super_class, super_function)
        statement.targets = [recursive_resolve_special_functions_expression(statement.targets[0], super_class, super_function)]
    elif type(statement) is ast.Return:
        statement.value = recursive_resolve_special_functions_expression(statement.value, super_class, super_function)
    elif type(statement) is ast.For:
        statement.iter = recursive_resolve_special_functions_expression(statement.iter, super_class, super_function)
    elif type(statement) is ast.While:
        statement.test = recursive_resolve_special_functions_expression(statement.test, super_class, super_function)
    elif type(statement) is ast.If:
        statement.test = recursive_resolve_special_functions_expression(statement.test, super_class, super_function)
    elif type(statement) is ast.Expr:
        statement.value = recursive_resolve_special_functions_expression(statement.value, super_class, super_function)


# Iterate over the entire AST replacing operators, special function calls and getters/setters with their function equivalent.
# Repl
def resolve_special_functions(_ast: ast.Module):

    for t, func in utils.function_iterator(_ast):
        for i in range(len(func.body)):


            # If the statement is an assign, we need to do a few tests and treat it slightly differently:
            if type(func.body[i]) is ast.Assign:
                # Firstly, chained assignments aren't supported just yet (i.e. x = y = 5)
                if len(func.body[i].targets) != 1:
                    raise errors.ChainedAssignmentNotImplemented

                # At this point there is exactly one target, so lets fetch it for brevity
                target = func.body[i].targets[0]

                if type(target) is ast.Subscript:
                    # If the target is a subscript, replace with the __setitem__ function

                    if type(target.value) is ast.Name:
                        if target.value.id == "self":
                            func.body[i] = ast.Expr(custom_nodes.SelfMemberFunction("__setitem__", [recursive_resolve_special_functions_expression(target.slice, t, func), recursive_resolve_special_functions_expression(func.body[i].value, t, func)]))
                            continue

                    func.body[i] = ast.Expr(custom_nodes.MemberFunction(recursive_resolve_special_functions_expression(target.value, t, func), "__setitem__", [
                        recursive_resolve_special_functions_expression(target.slice, t, func),
                        recursive_resolve_special_functions_expression(func.body[i].value, t, func)]))


                elif type(target) is ast.Attribute:
                    # If the target is an attribute and:
                    # - The attribute is self.SOMETHING and is NOT in an __init__ function
                    # - The attribute is not part of a function call (like a.b())
                    # - The attribute is not in its own setter
                    # Then we replace a.b = c with a.__set_b__(c)
                    # self.a = b stays as is.
                    # self.a.something = c maps to self.a.__set_something__(c)
                    # However, until we figure this mess out we will replace all and make no exceptions. It might be
                    # smarter to replace all a.b = c with a.__set_b__(c), then go back over the self.__set_SOMETHING__
                    # and set them back to self.something = for those that are in init or setter functions


                    # If the attribute is self.SOMETHING:

                    # If we have a self.SOMETHING inside an init or getter/setter function, do not replace with
                    # syntactic sugar as this will create infinitely recursive functions in getters/setters, and create
                    # translation problems in __init__.
                    if type(target.value) is ast.Name:


                        if t is not None:
                            if func.name == "__init__":
                                recursive_resolve_special_functions_statement(func.body[i], t, func)
                                continue
                            elif (func.name[:6] == "__get_" or func.name[:6] == "__set_") and func.name[-2:] == "__":
                                recursive_resolve_special_functions_statement(func.body[i], t, func)
                                continue

                        if type(target.value) is ast.Name:
                            if target.value.id == "self":
                                func.body[i] = ast.Expr(custom_nodes.SelfMemberFunction(f"__set_{target.attr}__", [recursive_resolve_special_functions_expression(func.body[i].value, t, func)]))
                                continue

                        func.body[i] = ast.Expr(custom_nodes.MemberFunction(
                            recursive_resolve_special_functions_expression(target.value, t, func), f"__set_{target.attr}__", [recursive_resolve_special_functions_expression(func.body[i].value, t, func)]))


                    else:
                        func.body[i] = ast.Expr(ast.Call(ast.Attribute(recursive_resolve_special_functions_expression(target.value, t, func), f"__set_{target.attr}__", ast.Store()), [recursive_resolve_special_functions_expression(func.body[i].value, t, func)], []))
                else:
                    recursive_resolve_special_functions_statement(func.body[i], t, func)
            else:
                recursive_resolve_special_functions_statement(func.body[i], t, func)


