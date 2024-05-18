import ast
# from builtins import function

import custom_nodes
import m_types
import mangler
import symbol_table
import ir
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
    m_types.Boolean(): {
        "_ZN8__bool__EF": m_types.Boolean(),
        "_ZN9__float__EF": m_types.Floating(),
        "_ZN7__int__EF": m_types.Integer(),
        "_ZN9__index__EF": m_types.ID(),
        "_ZN7__str__EF": m_types.String(),
        "_ZN7__fmt__EF": m_types.String(),
        "_ZN9__bytes__EF": m_types.Bytes(),

        "_ZN7__len__EF": m_types.ID(),

        "_ZN8__hash__EF": m_types.Integer(),

        "_ZN8__real__EF": m_types.Floating(),
        "_ZN8__imag__EF": m_types.Floating(),

        "_ZN7__one__EF": m_types.Boolean(),
        "_ZN8__zero__EF": m_types.Boolean(),
    },
    m_types.Floating(): {
        "_ZN7__add__EFf": m_types.Floating(),
    },
}

# Represents a code-generated user class complete with mangled name and dictionary of variable names to types
class UserClass:
    def __init__(self, identifier, member_types):
        self.identifier = identifier
        self.member_types = member_types

    def __repr__(self):
        return f"Class('{self.identifier}', {repr(self.member_types)})"

    def __call__(self):
        return self

    def mangle(self):
        mang = mangler.Class([self.member_types[x] for x in self.member_types], mangler.Name(self.identifier.get_name())).mangle()
        return mang




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




def deduce_class(class_name: str, constructor_args: list[m_types.MType], table: symbol_table.Table, ir_module: ir.Module, ir_function: ir.Function):

    # first we get the class table from the symbol table
    cl = table[class_name]

    # From the class table we obtain the table for the constructor
    init = cl["__init__"]

    mangled_init = mangler.Mangle("__init__", mangler.Function(constructor_args))

    print(mangled_init)

    init_function = ir.Function(mangled_init)



    type_map, _, _ = deduce_function(init, constructor_args, table, None, None, ir_module, init_function)

    members = {}

    for m in cl.member_variables:
        members["self." + m.name] = type_map["self." + m.name]

    mangled = mangler.Mangle(mangler.Name(class_name), mangler.Class([members[x] for x in members]))

    # Add the class to the ir
    ir_module.add_class(ir.Class(mangled, members))
    ir_module.add_member_function(mangled, init_function)


    return UserClass(mangled, members)

# Obtain the return value of the expression and recursively evaluate any function calls
def deduce_expression(expr: ast.expr, table: symbol_table.Table, function_table: symbol_table.Function, type_map: dict[str, m_types.MType], user_class: UserClass, ir_module: ir.Module, ir_function: ir.Function):
    if type(expr) is custom_nodes.MyCall:
        # Test to see if MyCall represents a global function call or a class construction
        if expr.id in table:
            entry = table[expr.id]

            # Get the types of all the arguments in the constructor
            arg_types = [deduce_expression(x, table, function_table, type_map, user_class, ir_module, ir_function) for x in expr.args]

            if type(entry) is symbol_table.Function:
                return deduce_function(expr.id, arg_types, table, ir_module, ir_function)
            elif type(entry) is symbol_table.Class:
                return deduce_class(expr.id, arg_types, table, ir_module, ir_function)
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
            return m_types.Integer()
        elif type(expr.value) is bool:
            return m_types.Boolean()
        elif type(expr.value) is float:
            return m_types.Floating()
        elif type(expr.value) is str:
            return m_types.String()
    elif type(expr) is ast.List:
        raise NotImplemented
    elif type(expr) is custom_nodes.MemberFunction:

        return deduce_member_function(expr, table, function_table, type_map, user_class, ir_module, ir_function)
    elif type(expr) is ast.Name:
        id = expr.id
        if id in type_map:
            return type_map[id]
        else:
            raise "Variable used before declaration"
    elif type(expr) is custom_nodes.SelfMemberVariable:

        return type_map["self." + expr.id]

    elif type(expr) is custom_nodes.SelfMemberFunction:
        print(type_map)
        print(user_class.identifier)
        return deduce_self_member_function(expr, table, function_table, type_map, user_class, ir_module, ir_function)
        raise NotImplemented


def deduce_generic_member(table: symbol_table.Table, function_table: symbol_table.Function, type_map, variant):

    # When dealing with member functions we have two cases.
    # a) self.member_function(...)
    # b) expression.member_function(...)
    # The user must supply different arguments depending on the case:
    # For self member functions we need:
    # - The 'type' of self, i.e. a UserClass
    # And for expression based member functions we need:
    # - A MemberFunction node
    # And in either case we need:
    # - A list of arguments
    # - the type of either self or the expression

    if variant == "self":
        # self.member_function(...)
        pass
    elif variant == "expr":
        # expression.member_function(...)
        # In this case we perform the built-in member function check
        pass

    pass

def deduce_member_function(node: custom_nodes.MemberFunction, table: symbol_table.Table, function_table: symbol_table.Function, type_map: dict[str, m_types.MType], user_class, ir_module: ir.Module, ir_function: ir.Function):



    expression_type = deduce_expression(node.exp, table, function_table, type_map, user_class, ir_module, ir_function)

    args_type = [deduce_expression(x, table, function_table, type_map, user_class, ir_module, ir_function) for x in node.args]

    print(type(expression_type))

    if type(expression_type) is not UserClass:
        if expression_type in built_in_returns:
            # the inner built_in_returns maps use mangled names, so we have to mangle the names:

            identifier = mangler.Mangle(mangler.Name(node.id), mangler.Function(args_type))

            if identifier in built_in_returns[expression_type]:
                return built_in_returns[expression_type][identifier]
            else:
                print(identifier)
                raise "Built in return type not in built_in_returns map"
        else:

            print(expression_type)

            raise "Built in return type not in built_in_returns map"
    else:

        mangled_name = expression_type.identifier

        print("t")
        print(mangled_name)

        identifier = mangler.Mangle(mangler.Name(node.id), mangler.Function(args_type))

        ir_function = ir.Function(identifier)

        print(ir_function)


        _, ret_type, _ = deduce_function(table[mangled_name.get_name()][node.id], args_type, table, expression_type.member_types, expression_type, ir_module, ir_function)

        ir_module.add_member_function(mangled_name, ir_function)

        return ret_type


def deduce_self_member_function(node: custom_nodes.SelfMemberFunction, table: symbol_table.Table, function_table: symbol_table.Function, type_map: dict[str, m_types.MType], user_class: UserClass, ir_module: ir.Module, ir_function: ir.Function):
    expression_type = user_class

    args_type = [deduce_expression(x, table, function_table, type_map, user_class, ir_module) for x in node.args]

    mangled_name = expression_type.identifier

    identifier = mangler.Mangle(mangler.Name(node.id), mangler.Function(args_type))

    ir_function = ir.Function(identifier)

    print("if")
    print(mangled_name)
    print(ir_function)

    ir_module.add_member_function(mangled_name, ir_function)
    print(ir_module)

    a, ret_type = deduce_function(table[mangled_name.get_name()][node.id], args_type, table,
                                  expression_type.member_types, expression_type, ir_module, ir_function)

    return ret_type





def deduce_function(function_table: symbol_table.Function, args: dict[str, m_types.MType], table: symbol_table.Table, member_vars: [str, m_types.MType], user_class: UserClass, ir_module: ir.Module, ir_function: ir.Function):

    func = function_table.ast_node

    return_type_set = set()

    if type(args) is dict:
        type_map = {**args}
    elif type(args) is list:
        # If the arguments are passed as a list instead of a map, convert into a map using the arguments as keys.
        type_map = {}

        # First we get a list of names of the parameters in order:
        params = [x.arg for x in function_table.ast_node.args.args]

        assert len(params) == len(args)

        for id, mtype in zip(params, args):
            type_map[id] = mtype



    if member_vars:
        for m in member_vars:
            type_map[m] = member_vars[m]


    # Dictionary mapping variable names to types. First we add the function args to this list

    ir_expression = None

    for stmt in func.body:
        if type(stmt) is ast.Assign:
            rhs = deduce_expression(stmt.value, table, function_table, type_map, user_class, ir_module, ir_function)

            if type(stmt.targets[0]) is ast.Name:
                type_map[stmt.targets[0].id] = rhs
            elif type(stmt.targets[0]) is custom_nodes.SelfMemberVariable:
                type_map["self." + stmt.targets[0].id] = rhs

        elif type(stmt) is ast.Return:

            if stmt:
                a= deduce_expression(stmt.value, table, function_table, type_map, user_class, ir_module, ir_function)

                return_type_set.add(a)
            else:
                raise "WE don't have a way to deal with void/() types yet. SHould probs work on that lol"
        elif type(stmt) is ast.Expr:
            deduce_expression(stmt.value, table, function_table, type_map, user_class, ir_module, ir_function)

    if len(return_type_set) == 0:
        ret_type = None
    elif len(return_type_set) == 1:
        ret_type = list(return_type_set)[0]
    else:
        raise "Functions must have one return type"

    return type_map, ret_type, ir_expression

def deduce_main(table: symbol_table.Table):

    ir_module = ir.Module()

    func_table = table["main"]

    type_map, _, _ = deduce_function(func_table, {}, table, None, None, ir_module, None)

    print(repr(ir_module))


'_ZN8__bool__EF'
'_ZN8__booL__EF'