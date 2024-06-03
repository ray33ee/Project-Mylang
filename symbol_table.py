import ast
import symtable

import errors
import members
import utils



# Get a list of all globals, i.e. all top level nodes - currently this is a tuple of a dictionary of
# name-function node pairs, and a dictionary of name-class node pairs,
def get_globals(_ast: ast.Module):
    functions = {}
    classes = {}

    for node in _ast.body:
        if type(node) is ast.FunctionDef:
            functions[node.name] = node
        if type(node) is ast.ClassDef:
            functions = {}
            for f in node.body:
                if type(f) is ast.FunctionDef:
                    functions[f.name] = f
            classes[node.name] = (node, functions)

    return functions, classes

# Signifies the location of a variable to exist on the stack
class StackVariable:
    pass


# Signifies the location of a variable to exist on the stack
class HeapVariable:
    pass


# Signifies the reference counting strategy is the standard kind (std::rc::Rc)
class StandardReferenceCounting:
    pass


# Signifies the reference counting strategy uses dumpster (dumpster::sync::Gc)
class DumpsterReferenceCounting:
    pass


# A class representing a variable in a symbol table
class Variable:
    def __init__(self, name):
        self.name = name
        self.type = None
        self.location = None
        self.rc_strategy = None
        self.is_parameter = None
        self.is_local = None
        self.is_self_variable = None  # True if a variable is a member variable in a class (self.SOMETHING)
        self.declaration = None  # A node in the python AST that points to the first assignment of the variable
        self.variables = []
        self.requirements = None # If the variable is a parameter, this will be filled with its requirements

    def __repr__(self):
        return self.name


# A class representing a function in a symbol table
class Function:
    def __init__(self, name, ast_node, table):
        self.name = name
        self.ast_node = ast_node
        self.variables = []

        for t in table.get_symbols():
            if type(t) is symtable.Symbol:
                # Only add variable symbols, not function calls
                if t.is_local():
                    print(t.get_name())
                    print(t.is_local())
                    self.variables.append(Variable(t.get_name()))

    def __str__(self):
        return f"{self.name} {self.ast_node} {self.variables}"

    def parameters(self):
        for variable in self.variables:
            if variable.is_parameter == True:
                yield variable

    def __contains__(self, item):
        for var in self.variables:
            if var.name == item:
                return True

        return False

    def __getitem__(self, item):
        for var in self.variables:
            if var.name == item:
                return var

        raise KeyError()





class Class:
    def __init__(self, name, node, functions, member_variables):
        self.name = name
        self.functions = functions
        self.node = node
        self.member_variables = member_variables

    def __contains__(self, item):

        for func in self.functions:
            if func.name == item:
                return True

        return False

    def __getitem__(self, item):
        for func in self.functions:
            if func.name == item:
                return func

        raise KeyError()

# Mylang tables are simpler than python tables, since python allows nested functions, classes, and all sorts of
# topologies, whereas mylang does not. Mylang can have a list of functions and a list of classes. Each class contains
# a list of functions. Each function contains a list of variables. This structure is emulated in the Table class:
class Table:
    def __init__(self, _ast: ast.Module, table: symtable.SymbolTable):
        self.functions = []
        self.classes = []

        function_nodes, class_nodes = get_globals(_ast)

        member_variables = members.resolve_members(_ast)

        print("mem")
        print(member_variables)

        for t in table.get_children():
            if type(t) is symtable.Function:
                self.functions.append(Function(t.get_name(), function_nodes[t.get_name()], t))
            if type(t) is symtable.Class:
                node, class_function_nodes = class_nodes[t.get_name()]


                class_functions = []

                for f in t.get_children():
                    class_functions.append(Function(f.get_name(), class_function_nodes[f.get_name()], f))

                self.classes.append(Class(t.get_name(), node, class_functions, list(map(lambda x: Variable(x), member_variables[t.get_name()]))    ))




    def get_main(self):
        try:
            return self["main"]
        except KeyError:
            raise errors.MainFunctionMissing()

    def __str__(self):
        s = ""
        for f in self.functions:
            s += str(f) + "\n"
            for v in f.variables:
                s += "    " + str(v) + "\n"

        for c in self.classes:
            s += f"{c.name} {c.node}\n"

            for m in c.member_variables:
                s += "    " + str(m) + " <Class Member Variable>\n"

            for f in c.functions:
                s += "    " + str(f) + "\n"
                for v in f.variables:
                    s += "        " + str(v) + "\n"
        return s


    def __contains__(self, item):

        for func in self.functions:
            if func.name == item:
                return True

        for cl in self.classes:
            if cl.name == item:
                return True

        return False

    def __getitem__(self, item):
        for func in self.functions:
            if func.name == item:
                return func

        for cl in self.classes:
            if cl.name == item:
                return cl

        raise KeyError()

