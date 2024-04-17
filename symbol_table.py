import ast
import symtable

import utils


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
    def __init__(self, name, declaration_node):
        self.name = name
        self.type = None
        self.location = None
        self.rc_strategy = None
        self.is_parameter = None
        self.is_local = None
        self.is_self_variable = None  # True if a variable is a member variable in a class (self.SOMETHING)
        self.declaration = declaration_node  # A node in the python AST that points to the first assignment of the variable
        self.variables = []


# A class representing a function in a symbol table
class Function:
    def __init__(self, name, ast_node, table):
        self.name = name
        self.ast_node = ast_node
        self.variables = []

        print(table)

        for t in table.get_symbols():
            print("pokpkop")
            if type(t) is symtable.Symbol:
                self.variables.append(t.get_name())

    def __str__(self):
        return f"{self.name} {ast.dump(self.ast_node)} {self.variables}"

    def parameters(self):
        for variable in self.variables:
            if variable.is_parameter == True:
                yield variable


class Class:
    def __init__(self, name, node, functions):
        self.name = name
        self.functions = functions
        self.node = node

# Todo: Make sure Table adds self.VARIABLEs to the symbol tables, and doesnt add 'self' on its own unless its used on its own

# Mylang tables are simpler than python tables, since python allows nested functions, classes, and all sorts of
# topologies, whereas mylang does not. Mylang can have a list of functions and a list of classes. Each class contains
# a list of functions. Each function contains a list of variables. This structure is emulated in the Table class:
class Table:
    def __init__(self, _ast: ast.Module, table: symtable.SymbolTable):
        self.functions = []
        self.classes = []

        function_nodes, class_nodes = utils.get_globals(_ast)

        for t in table.get_children():
            if type(t) is symtable.Function:
                self.functions.append(Function(t.get_name(), function_nodes[t.get_name()], t))
            if type(t) is symtable.Class:
                node, class_function_nodes = class_nodes[t.get_name()]

                class_functions = []

                for f in t.get_children():
                    class_functions.append(Function(f.get_name(), class_function_nodes[f.get_name()], f))

                self.classes.append(Class(t.get_name(), node, class_functions))

        for f in self.functions:
            print(f)

        for c in self.classes:
            print(f"{c.name} {ast.dump(c.node)}")
            for f in c.functions:
                print("    " + str(f))