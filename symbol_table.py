

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


# A class representing a function in a symbol table
class Function:
    def __init__(self, name, ast_node):
        self.name = name
        self.ast_node = ast_node


# A class representing a variable in a symbol table
class Variable:
    def __init__(self, name, declaration_node):
        self.name = name
        self.location = None
        self.rc_strategy = None
        self.is_parameter = None
        self.is_local = None
        self.is_self_variable = None  # True if a variable is a member variable in a class (self.SOMETHING)
        self.declaration = declaration_node  # A node in the python AST that points to the first assignment of the variable
        self.uses = []  # List of AST nodes that reference the variable
