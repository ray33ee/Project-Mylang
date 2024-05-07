import ast


# Represents a single function requirement on a variable
class FunctionRequirement:
    def __init__(self, name, args, ret):
        self.name = name
        self.args = args
        self.ret = ret


    def pretty(self, level=0, indent=4):
        ags = "["
        print(self.args)
        for a in self.args:
            ags += a.pretty(level+1, indent) + "\n"
        ags += (level+1) * indent * " " + "]"
        return f"""FunctionRequirement(
{(level+1) * indent * " "}'name': {self.name}
{(level+1) * indent * " "}'args': {ags})
{(level+1) * indent * " "}'ret': {self.ret.pretty(level+1, indent) if self.ret else ""}"""

# Abstract class representing a particular requirement on a variable
class Requirement:
    # Display the requrirement nicely with indentation
    def pretty(self, level=0, indent=4):
        pass

# Respresents the strictest type of requirement, an explicit type declaration
class ExplicitType(Requirement):
    def __init__(self, m_type):
        self.m_type = m_type

# Represents the most common type of requirement, a list of functions that the variable must implement
class Functions(Requirement):
    def __init__(self, funcs):
        self.funcs = funcs

# Represents the most generic type of requirement, no requirements at all
class NoRequirement(Requirement):
    pass

# Represents a requirement placeholder, used during parsing if a requirement has not yet been identified
class Placeholder(Requirement):
    pass


def process_expr(expr: ast.Expr, symbols):

    t = type(expr)

    if t is ast.Call:
        # If expression is x.y(...) where x is in arguments, we have a requirement
        if type(expr.func) is ast.Attribute:
            if type(expr.func.value) is ast.Name:
                if expr.func.value.id in symbols:
                    print(f"Member function found for '{expr.func.value.id}' named '{expr.func.attr}' with args '{expr.args}'")

                    requirements = [process_expr(a, symbols) for a in expr.args]

                    req = FunctionRequirement(expr.func.attr, requirements, None)

                    # symbols[expr.func.value.id] = req

                    return req


            elif type(expr.func.value) is ast.Call:
                # If expression is x.something(...).something_else()

                print("Pokpok")

                for a in expr.func.value.args:
                    print(process_expr(a, symbols).pretty())

                ret = FunctionRequirement(expr.func.attr, [process_expr(a, symbols) for a in expr.func.value.args], process_expr(expr.func.value, symbols))


                return ret


        elif type(expr.func) is ast.Name:
            # If the expression is y(x) where x is an argument, we have a requirement based on the requirements of y
            for func_arg in expr.args:
                if type(func_arg) is ast.Name:
                    if func_arg.id in symbols:
                        print(f"Argument {func_arg.id} found in function call {expr.func.id}")
                        return None

    if t is ast.IfExp:
        raise NotImplemented
    elif t is ast.Dict:
        raise NotImplemented
    elif t is ast.Set:
        raise NotImplemented
    elif t is ast.List:
        raise NotImplemented
    elif t is ast.Compare:
        raise NotImplemented
    elif t is ast.Call:
        print(ast.dump(expr))

        raise NotImplemented
    elif t is ast.Constant:
        raise NotImplemented
    elif t is ast.Name:
        raise NotImplemented
    else:
        print(ast.dump(expr))
        raise NotImplemented


# Take a single statement from a function
def process_statement(stmt: ast.stmt, symbols):

    t = type(stmt)

    # Firstly, if the statement is an assign, check to see if it creates an alias for `argument`
    if t is ast.Assign:
        if type(stmt.value) is ast.Name:
            if stmt.value.id in symbols:
                print(f"Alias for {stmt.value.id} found ({stmt.targets[0].id})")
                # Add the new alias to the symbols list, with the aliased requirements as its own requirements.
                # This way changing the requirements of either alias or aliased value will change both.
                symbols[stmt.targets[0].id] = symbols[stmt.value.id]
                return


    if t is ast.Assign:
        raise NotImplemented
    elif t is ast.Return:
        raise NotImplemented
    elif t is ast.AugAssign:
        raise NotImplemented
    elif t is ast.For:
        raise NotImplemented
    elif t is ast.While:
        raise NotImplemented
    elif t is ast.If:
        raise NotImplemented
    elif t is ast.Expr:
        # If a statement is an expression, then its return value (if it even has one) is ignored. So we only then recursively look into the expression contents
        return process_expr(stmt.value, symbols)

# Takes a function and an argument in that function, and returns a type implementing Requirement
#
def resolve_function(function: ast.FunctionDef):

    # Symbol is a dictionary mapping any function paramaters, return value decendents and aliases to their requirements
    symbols = {}

    # Initialise the symbol dict with the function arguments
    for arg in function.args.args:
        symbols[arg.arg] = None

    for statement in function.body:
        print(process_statement(statement, symbols).pretty())

    print(symbols)