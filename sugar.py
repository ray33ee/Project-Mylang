import utils
import ast

def recursive_resolve_special_functions_expression(expression):

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
        return ast.Call(
            ast.Attribute(recursive_resolve_special_functions_expression(expression.left), binary_op_mapping[type(expression.op)], ast.Load()),
            [recursive_resolve_special_functions_expression(expression.right)],
            [])
    elif type(expression) is ast.Attribute:
        return ast.Call(ast.Attribute(recursive_resolve_special_functions_expression(expression.value),
                                      f"__get_{expression.attr}__", expression.ctx), [], [])
    elif type(expression) is ast.UnaryOp:
        return ast.Call(ast.Attribute(recursive_resolve_special_functions_expression(expression.operand), unary_op_mapping[type(expression.op)], ast.Load()), [], [])
    elif type(expression) is ast.Compare:

        if len(expression.ops) != 1 or len(expression.comparators) != 1:
            raise "Number of operators and number of RHS comparators in ast.Compare must be 1. Chained comparison is not allowed"

        left = recursive_resolve_special_functions_expression(expression.left)
        right = recursive_resolve_special_functions_expression(expression.comparators[0])

        return ast.Call(ast.Attribute(left, compare_op_mapping[type(expression.ops[0])], ast.Load()), [right], [])


    elif type(expression) is ast.Call:
        if type(expression.func) is ast.Name:
            func_name = expression.func.id

            if func_name in built_in_set:
                print(ast.dump(expression.args[0]))
                # replace FUNCTION(x) with x.__FUNCTION__()
                return ast.Call(ast.Attribute(recursive_resolve_special_functions_expression(expression.args[0]), f"__{func_name}__", ast.Load()), [], [])
            else:
                return ast.Call(expression.func, [recursive_resolve_special_functions_expression(x) for x in expression.args], expression.keywords)
        elif type(expression.func) is ast.Attribute:
            return ast.Call(expression.func,
                            [recursive_resolve_special_functions_expression(x) for x in expression.args], expression.keywords)
        else:
            print(expression.func)
            raise NotImplemented
    elif type(expression) is ast.IfExp:
        return ast.IfExp(
            recursive_resolve_special_functions_expression(expression.test),
            recursive_resolve_special_functions_expression(expression.body),
            recursive_resolve_special_functions_expression(expression.orelse)
        )
    elif type(expression) is ast.Subscript:
        if type(expression.ctx) == ast.Load:
            return ast.Call(
                ast.Attribute(recursive_resolve_special_functions_expression(expression.value),
                              "__getitem__",
                              ast.Load()), [recursive_resolve_special_functions_expression(expression.slice)], [])
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
    elif type(expression) is ast.Name or type(expression) is ast.Constant:
        return expression
    elif type(expression) is ast.Slice:
        raise NotImplemented
    else:
        print(f"Expression {type(expression)} not supported")
        raise "Error"


def recursive_resolve_special_functions_statement(statement):
    if type(statement) is ast.Assign:
        statement.value = recursive_resolve_special_functions_expression(statement.value)
    elif type(statement) is ast.Return:
        statement.value = recursive_resolve_special_functions_expression(statement.value)
    elif type(statement) is ast.For:
        statement.iter = recursive_resolve_special_functions_expression(statement.iter)
    elif type(statement) is ast.While:
        statement.test = recursive_resolve_special_functions_expression(statement.test)
    elif type(statement) is ast.If:
        statement.test = recursive_resolve_special_functions_expression(statement.test)
    elif type(statement) is ast.Expr:
        statement.value = recursive_resolve_special_functions_expression(statement.value)


# Iterate over the entire AST replacing operators, special function calls and getters/setters with their function equivalent.
# Repl
def resolve_special_functions(_ast: ast.Module):
    our_map = {}

    for t, func in utils.function_iterator(_ast):
        for i in range(len(func.body)):


            # If the statement is an assign, we need to do a few tests and treat it slightly differently:
            if type(func.body[i]) is ast.Assign:
                # Firstly, chained assignments aren't supported just yet (i.e. x = y = 5)
                if len(func.body[i].targets) != 1:
                    raise "Invalid number of assignment targets. We do not support chained assignment yet"

                # At this point there is exactly one target, so lets fetch it for brevity
                target = func.body[i].targets[0]


                if type(target) is ast.Subscript:
                    # If the target is a subscript, replace with the __setitem__ function
                    func.body[i] = ast.Expr(ast.Call(ast.Attribute(recursive_resolve_special_functions_expression(target.value),
                              "__setitem__",
                              ast.Store()), [recursive_resolve_special_functions_expression(target.slice), recursive_resolve_special_functions_expression(func.body[i].value)], []))
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
                    func.body[i] = ast.Expr(ast.Call(ast.Attribute(recursive_resolve_special_functions_expression(target.value), f"__set_{target.attr}__", ast.Store()), [recursive_resolve_special_functions_expression(func.body[i].value)], []))
                else:
                    recursive_resolve_special_functions_statement(func.body[i])
            else:
                recursive_resolve_special_functions_statement(func.body[i])


