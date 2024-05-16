import ast
# from builtins import function

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

# Represents a code-generated user class complete with mangled name and dictionary of variable names to types
class UserClass:
    def __init__(self, identifier, member_types):
        self.identifier = identifier
        self.member_types = member_types

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




def deduce_class(class_name: str, constructor_args: list[m_types.MType], table: symbol_table.Table):

    print(class_name)
    print(constructor_args)

    # first we get the class table from the symbol table
    cl = table[class_name]

    # From the class table we obtain the table for the constructor
    init = cl["__init__"]

    type_map, _ = deduce_function(init, constructor_args, table, None)

    members = {}

    for m in cl.member_variables:
        members["self." + m.name] = type_map["self." + m.name]


    mangle = mangler.Mangler()

    mangled = mangle(mangler.Name(class_name), mangler.Class([members[x]() for x in members]))

    return UserClass(mangled, members)

# Obtain the return value of the expression and recursively evaluate any function calls
def deduce_expression(expr: ast.expr, table: symbol_table.Table, function_table: symbol_table.Function, type_map: dict[str, m_types.MType]):
    if type(expr) is custom_nodes.MyCall:
        # Test to see if MyCall represents a global function call or a class construction
        if expr.id in table:
            entry = table[expr.id]

            # Get the types of all the arguments in the constructor
            arg_types = [deduce_expression(x, table, function_table, type_map) for x in expr.args]

            if type(entry) is symbol_table.Function:
                return deduce_function(expr.id, arg_types, table)[1]
            elif type(entry) is symbol_table.Class:
                return deduce_class(expr.id, arg_types, table)
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
            raise "Variable used before declaration"
    elif type(expr) is custom_nodes.SelfMemberVariable:



        print("typemap")
        print(type_map)

        return type_map["self." + expr.id]

    elif type(expr) is custom_nodes.SelfMemberFunction:
        raise NotImplemented




def deduce_member_function(node: custom_nodes.MemberFunction, table: symbol_table.Table, function_table: symbol_table.Function, type_map: dict[str, m_types.MType]):



    expression_type = deduce_expression(node.exp, table, function_table, type_map)

    args_type = [deduce_expression(x, table, function_table, type_map)() for x in node.args]

    print(expression_type)

    if type(expression_type) is not UserClass:
        if expression_type in built_in_returns:
            # the inner built_in_returns maps use mangled names, so we have to mangle the names:
            m = mangler.Mangler()

            identifier = m(mangler.Name(node.id), mangler.Function(args_type))

            if identifier in built_in_returns[expression_type]:
                return built_in_returns[expression_type][identifier]
            else:
                raise "Built in return type not in built_in_returns map"
        else:



            raise "Built in return type not in built_in_returns map"
    else:

        mangled_name = expression_type.identifier
        member_variables = expression_type.member_types

        print("name")
        print(mangled_name)
        print(type(mangled_name))

        print("member types")
        print(member_variables)

        print("member function")
        print(node.id)

        print("member function table")
        print(table[mangled_name.get_name()][node.id])

        a, ret_type = deduce_function(table[mangled_name.get_name()][node.id], args_type, table, expression_type.member_types)

        print("a")
        print(a)

        print("return type")
        print(ret_type)

        return ret_type


def deduce_function(function_table: symbol_table.Function, args: dict[str, m_types.MType], table: symbol_table.Table, member_vars: [str, m_types.MType]):

    func = function_table.ast_node

    return_type_set = set()

    if type(args) is dict:
        type_map = {**args}
    elif type(args) is list:
        # If the arguments are passed as a list instead of a map, convert into a map using the arguments as keys.
        type_map = {}

        # First we get a list of names of the parameters in order:
        params = [x.arg for x in function_table.ast_node.args.args]

        print("Params")
        print(params)

        assert len(params) == len(args)

        for id, mtype in zip(params, args):
            type_map[id] = mtype

        print(type_map)

    if member_vars:
        for m in member_vars:
            type_map[m] = member_vars[m]

    print("function - typemap")
    print(type_map)


    # Dictionary mapping variable names to types. First we add the function args to this list


    for stmt in func.body:
        print(ast.dump(stmt))
        if type(stmt) is ast.Assign:
            rhs = deduce_expression(stmt.value, table, function_table, type_map)

            if type(stmt.targets[0]) is ast.Name:
                type_map[stmt.targets[0].id] = rhs
            elif type(stmt.targets[0]) is custom_nodes.SelfMemberVariable:
                type_map["self." + stmt.targets[0].id] = rhs

        if type(stmt) is ast.Return:

            if stmt:
                return_type_set.add(deduce_expression(stmt.value, table, function_table, type_map))
            else:
                raise "WE don't have a way to deal with void/() types yet. SHould probs work on that lol"


    return type_map, return_type_set

def deduce_main(table: symbol_table.Table):

    func_table = table["main"]

    type_map, _ = deduce_function(func_table, {}, table, None)

    print(type_map)


'_ZN8__bool__EF'
'_ZN8__booL__EF'