import ast

import custom_nodes
import m_types
import mangler
import symbol_table

import itertools

# Represents a return value that depends on the type of object. For example, take the `__getitem__` in a vector<T>.
# The return value of this type is dependent on the inner type in the vector, i.e. T. So this is represented with
# ReturnBound(0) where 0 represents the 1st generic type. To represent the value in a Map<K, V>, ReturnBound(1) where
# 1 represents the second generic type (first generic type is the key type, second is the value type)
class ReturnBound:
    def __init__(self, index):
        self.index = index

# The following dictionary maps types to another dictionary which itself maps mangled names to their return values
built_in_returns = {
    m_types.Boolean: {
        "_ZN8__bool__EF": m_types.Boolean,
        "_ZN9__float__EF": m_types.Floating,
        "_ZN7__int__EF": m_types.Integer,
        "_ZN9__index__EF": m_types.ID,
        "_ZN7__str__EF": m_types.String,
        "_ZN7__fmt__EF": m_types.String,
        "_ZN9__bytes__EF": m_types.Bytes,

        "_ZN7__len__EF": m_types.ID,

        "_ZN8__hash__EF": m_types.Integer,

        "_ZN8__real__EF": m_types.Floating,
        "_ZN8__imag__EF": m_types.Floating,

        "_ZN7__one__EF": m_types.Boolean,
        "_ZN8__zero__EF": m_types.Boolean,
    },
    "int": {

    },
}


# Certain types such as lists, sets and dictionaries take a list of expressions. For these types, every expression in
# each list must have the same type, T. Here we a) check that all are the same type and b) return the common type. An
# exception is raised if not
def verify_list(args: list[ast.expr], table, function_table, type_map):

    def acc(x, y):
        y = deduce_expression(y, table, function_table, type_map)
        if x is None:
            return y
        if x is not y:
            raise "All values must be same type"
        return y

    return itertools.accumulate(args, acc)




def deduce_class(class_name: str, table: symbol_table.Table, constructor_args: list[m_types.MType]):

    raise NotImplemented

# Obtain the return value of the expression and recursively evaluate any function calls
def deduce_expression(expr: ast.expr, table: symbol_table.Table, function_table: symbol_table.Table, type_map: dict[str, m_types.MType]):
    if type(expr) is custom_nodes.MyCall:
        # Test to see if MyCall represents a global function call or a class construction
        if expr.id in table:
            entry = table[expr.id]
            if type(entry) is symbol_table.Function:
                print("Function call " + entry.name)
                raise NotImplemented
            elif type(entry) is symbol_table.Class:

                # Get the types of all the arguments in the constructor
                arg_types = [deduce_expression(x, table, function_table, type_map) for x in expr.args]

                return deduce_class(entry, table, arg_types)
            else:
                raise "unreachable"
        else:
            # If not, the only possibility is that MyCall represents a callable object
            if expr.id in function_table:
                # Here we treat a(...) as a.__call__(...)
                if expr.id in type_map:
                    raise NotImplemented
                else:
                    # If the variable is not declared or the type is unknown, this is a compile error
                    raise "error"
            else:
                # There are only three possibilities for an expression like 'a()', global function call, constructor, callable object.
                # If it's not those three, we have an error
                raise "error"
    elif type(expr) is ast.Constant:
        if type(expr.value) is int:
            return m_types.Integer
        elif type(expr.value) is bool:
            return m_types.Boolean
        elif type(expr.value) is float:
            return m_types.Floating
        elif type(expr.value) is str:
            return m_types.String
    elif type(expr) is ast.List:
        raise NotImplemented
    elif type(expr) is custom_nodes.MemberFunction:
        return deduce_member_function(expr, table, function_table, type_map)
    elif type(expr) is ast.Name:
        id = expr.id
        if id in type_map:
            return type_map[id]
        else:
            raise "Varable used before declaration"




def deduce_member_function(node: custom_nodes.MemberFunction, table: symbol_table.Table, function_table: symbol_table.Table, type_map: dict[str, m_types.MType]):
    expression_type = deduce_expression(node.exp, table, function_table, type_map)

    args_type = [deduce_expression(x, table, function_table, type_map)() for x in node.args]

    if expression_type in built_in_returns:
        # the inner built_in_returns maps use mangled names, so we have to mangle the names:
        m = mangler.Mangler()

        identifier = m(mangler.Name(node.id), mangler.Function(args_type))

        return built_in_returns[expression_type][identifier]
    else:
        raise NotImplemented


def deduce_function(func_name: str, args: dict[str, m_types.MType], table: symbol_table.Table):

    function_table = table[func_name]
    func = function_table.ast_node

    # Dictionary mapping variable names to types. First we add the function args to this list
    type_map = {**args}

    for stmt in func.body:
        print(ast.dump(stmt))
        if type(stmt) is ast.Assign:
            rhs = deduce_expression(stmt.value, table, function_table, type_map)

            if type(stmt.targets[0]) is ast.Name:
                type_map[stmt.targets[0].id] = rhs

    return type_map, None

def deduce_main(table: symbol_table.Table):

    type_map, _ = deduce_function("main", {}, table)

    print(type_map)


'_ZN8__bool__EF'
'_ZN8__booL__EF'